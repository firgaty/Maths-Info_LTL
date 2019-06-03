from ast import *
from graph import *
from copy import *
from formulas import *


def is_in_list(ast, li):
    for l in li:
        if l.is_same(ast):
            return True
    return False


def is_in_trans_list(d, trans):
    x, y = trans
    for (a, b) in d:
        if a == x and b == y:
            return True
    return False


def node_in_list(n, li):
    for e in li:
        if e.nb == n.nb:
            return True
    return False


def is_same_list(li1, li2):
    for e in li1:
        if not is_in_list(e, li2):
            return False

    for e in li2:
        if not is_in_list(e, li1):
            return False

    # print("ok")
    return True


def remove_from_list(remove, frm):
    for e in remove:
        for i in range(len(frm)):
            if e.is_same(frm[i]):
                frm.pop(i)
                break
    return frm


def union(l1, l2):
    for e in l1:
        if not is_in_list(e, l2):
            l2.append(e)
    return l2


def node_union(l1, l2):
    for e in l1:
        if not node_in_list(e, l2):
            l2.append(e)
    return l2


def trans_union(l1, l2):
    for e in l1:
        if not is_in_trans_list(l2, e):
            l2.append(e)
    return l2


def curr1(ast):
    if type(ast) == Until:
        return [ast.left]
    if type(ast) == Release:
        return [ast.right]
    if type(ast) == Or:
        return [ast.right]
    return [ast]


def next1(ast):
    if type(ast) == Until or type(ast) == Release:
        return [ast]
    return []


def curr2(ast):
    if type(ast) == Until:
        return [ast.right]
    if type(ast) == Release:
        return [ast.left, ast.right]
    if type(ast) == Or:
        return [ast.left]
    return []


class Init(Expr0):
    def __init__(self):
        super(Init, self).__init__("init")


class Node(object):
    def __init__(self, ast, nb, incoming=None):
        self.ast = ast
        self.nb = nb
        self.incoming = []
        self.next = []
        self.now = []

    def is_same(self, node):
        return node.ast.is_same(self.ast)

    def __str__(self):
        s = "[ " + str(self.nb) + ": " + str(self.ast) + ", " + "|"
        for e in self.incoming:
            s += str(e.nb) + ", "
        s += "|"
        for e in self.now:
            s += str(e) + ", "
        s += "|"
        for e in self.next:
            s += str(e) + ", "
        s += "|"
        s += " ]"
        return s


class Gerth:
    def __init__(self, ast):
        self.ast = ast
        self.nodes = []
        self.automaton = GBA()
        self.nb = 1
        self.formula = Formula(deepcopy(ast))

    def to_string(self):
        s = "{\n"
        for e in self.nodes:
            s += str(e) + "\n"
        s += "}"
        return s

    def __str__(self):
        return self.to_string()

    def new_node(self, ast):
        # print("new node")
        out = Node(ast, self.nb)
        self.nodes.append(out)
        self.nb += 1
        return out

    def any_node_has(self, nxt, old):
        s = ''
        for e in nxt:
            s += str(e) + "|"

        s += "\n"
        for e in old:
            s += str(e) + "|"

        # print(s)
        for n in self.nodes:
            if is_same_list(old, n.now):
                # print("old <-> n.now")
                if is_same_list(nxt, n.next):
                    # print("nxt <-> n.next")
                    return n
        # print("None..")
        return None

    def expand(self, curr, old, nxt, incoming):
        # for e in curr:
        #     print(str(e))
        # print(str(self))
        if len(curr) == 0:
            q = self.any_node_has(nxt, old)
            if q != None:
                q.incoming = node_union(deepcopy(incoming), q.incoming)
            else:
                q = self.new_node(None)
                q.incoming = deepcopy(incoming)
                q.now = deepcopy(old)
                q.next = deepcopy(nxt)
                # print(str(q))
                self.expand(nxt, [], [], [q])
        else:
            f = curr.pop(0)
            old = union([f], old)

            if type(f) == Top or type(f) == Bottom or type(f) == Var or (type(f) == Not and type(f.right) == Var):
                if type(f) == Bottom or is_in_list(Not(f).simplify_not(), old):
                    pass
                else:
                    self.expand(curr, old, nxt, incoming)
            elif type(f) == And:
                self.expand(union(remove_from_list(
                    old, [f.left, f.right]), curr), old, nxt, incoming)
            elif type(f) == Next:
                self.expand(curr, old, union([f.right], nxt), incoming)
            elif type(f) == Or or type(f) == Until or type(f) == Release:
                un = union(remove_from_list(old, curr1(f)), curr)
                self.expand(un, old, union(next1(f), nxt), incoming)
                self.expand(union(remove_from_list(
                    old, curr2(f)), curr), old, nxt, incoming)
        return

    def create_graph(self):
        ini = Node(Init(), 0)
        self.expand([self.ast], [], [], [ini])
        self.nodes.insert(0, ini)
        return

    def __label(self, node):
        l = []
        for e in node.now:
            if type(e) == Var or type(e) == Top or type(e) == Bottom or type(e) == Not and (type(e) == Var or type(e) == Top or type(e) == Bottom):
                if not is_in_list(Not(e).simplify_not(), node.now):
                    l.append(e)
        # if len(l) == 0:
        #     return [Bottom()]
        for e in l:
            if type(e) == Top:
                return [Top()]
        return l

    def __transition(self, node):
        d = []
        for e in node.incoming:
            if not is_in_trans_list(d, (e.nb, node.nb)):
                d.append((e.nb, node.nb))
        return d

    def __repeated(self, U, node):
        for e in U:
            if is_in_list(e.right, node.now) or not is_in_list(e, node.now):
                return True
        return False

    def __initial(self, node):
        for e in node.incoming:
            if e.nb == 0:
                return True
        return False

    def __get_label(self, labels, i):
        for (n, l) in labels:
            # print(str(n))
            if n == i:
                return l
        return []

    def gba(self):
        g = GBA()

        L = []
        D = []
        I = []
        F = []
        U = []

        # On récupère les Until dans une liste
        for e in self.formula.posf_list:
            if type(e) == Until:
                U.append(e)

        for e in self.nodes:
            g.add_vertex(e.nb)
            L.append((e.nb, self.__label(e)))
            D = trans_union(D, self.__transition(e))
            if self.__initial(e):
                I.append(e.nb)
                g.add_init(e.nb)
            if self.__repeated(U, e):
                F.append(e.nb)
                g.add_repeated(e.nb)

        print(str(I))

        for (a, b) in D:
            g.add_edge([a, b, self.__get_label(L, b)])
            print(str([a, b, self.__get_label(L, b)]))

        return g
