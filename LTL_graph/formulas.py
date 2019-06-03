from ast import *
from graph import *
import itertools


class Formula(object):
    # TODO effets de bord
    def __init__(self, ast):
        self.ast = ast
        self.posf_list = []  # Positive formulas.
        self.negf_list = []
        self.atoms = []
        self.pos_1 = 0
        self.gen_formulas()

    # check si la formule ou la negation de la formule est déjà dans
    # la liste des sous formules
    def __is_in_list(self, ast, li):
        for l in li:
            if l.is_same(ast):
                return True
        return False

    def add(self, ast):
        if type(ast) == Not:
            ast = ast.right
        if type(ast) == Top or type(ast) == Bottom:
            return True
        if (self.__is_in_list(ast, self.posf_list)):
            return False
        self.posf_list.append(ast)
        return True

    def __gen_formulas(self, ast):
        self.add(ast)
        if type(ast) == Until:
            # Cloture de aUb par X(aUb)
            self.add(Next(ast))
        if ast.left != None:
            self.__gen_formulas(ast.left)
        if ast.right != None:
            self.__gen_formulas(ast.right)

    def gen_formulas(self):
        self.__gen_formulas(self.ast)
        self.sort_pos()
        self.gen_negf()

    def to_string(self, list_type=0, atoms=None):
        if list_type == 3:
            if atoms == None:
                return ''
            s = '|'
            for e in atoms:
                if (type(e) is not Not):
                    s += " "
                s += " " + e.to_string() + " |"
            return s

        s = "[|"
        if list_type == 0:
            for l in self.posf_list:
                if (type(l) is not Not):
                    s += " "
                s += " " + l.to_string() + " |"
        elif list_type == 1:
            for l in self.negf_list:
                if (type(l) is not Not):
                    s += " "
                s += " " + l.to_string() + " |"
        elif list_type == 2:
            s += "\n"
            for l in self.atoms:
                s += "{|"
                for e in l:
                    if (type(e) is not Not):
                        s += " "
                    s += " " + e.to_string() + " |"
                s += "},\n"
        s += "]"
        return s

    def sort_pos(self):
        # Tri les variables et les Next devant.
        self.posf_list.sort(
            key=lambda x: x.get_logic_height(True), reverse=False)

        l = len(self.posf_list) 
        i = 0
        if l > 0:
            while i < l and self.posf_list[i].get_logic_height() == 1:
                i += 1

        self.pos_1 = i
        # Tri des variables devant les Next.
        self.posf_list[0:i] = sorted(
            self.posf_list[0:i], key=lambda x: x.get_height(True), reverse=False)

    def gen_negf(self):
        for ast in self.posf_list:
            self.negf_list.append(Not(ast).simplify()[0])

# P in A <=> not P not in A
# P1 v P2 in A <=> P1 in a v P2 in A
# P1 U P2 in A <=> P2 in a v (P1 in a & X(P1 U P2) in a)

    def __gen_atom(self, atom, n):
        ast = self.posf_list[n]
        if type(ast) == Until:
            if type(ast.right) == Top or self.__is_in_list(ast.right, atom) \
                or ((type(ast.left) == Top or self.__is_in_list(ast.left, atom))
                    and self.__is_in_list(Next(ast), atom)):
                atom.append(ast)
            else:
                atom.append(self.negf_list[n])
        elif type(ast) == Or:
            if type(ast.left) == Top or type(ast.right) == Top \
                    or self.__is_in_list(ast.left, atom) or self.__is_in_list(ast.right, atom):
                atom.append(ast)
            else:
                atom.append(self.negf_list[n])

    def gen_atoms(self):
        for values in itertools.product([True, False], repeat=self.pos_1):
            atom = []
            for i in range(self.pos_1):
                if values[i]:
                    atom.append(self.posf_list[i])
                else:
                    atom.append(self.negf_list[i])

            for i in range(self.pos_1, len(self.posf_list)):
                self.__gen_atom(atom, i)
            self.atoms.append(atom)
        return

    def get_atoms(self):
        return self.atoms

    def __atom_is_init(self, atom):
        for e in atom:
            if e.is_same(self.ast):
                return True
        return False

    def __atom_is_repeated(self, atom):
        for e in self.posf_list:
            if (type(e) == Until):
                if (self.__is_in_list(e.right, atom) or self.__is_in_list(Not(e), atom)):
                    return True
        return False

    def __atom_has_edge(self, atom1, atom2):
        # print(self.to_string(3, atom1))
        # print(self.to_string(3, atom2))
        
        for e in atom1:
            if (type(e) == Next):
                if not self.__is_in_list(e.right, atom2):
                    # print("atom1.1")
                    return False
            if (type(e) == Not and type(e.right) == Next):
                if not self.__is_in_list(Not(e.right).simplify()[0], atom2):
                    # print("atom1.2")
                    return False
                # if (self.__is_in_list(e, atom1) and self.__is_in_list(Not(e.right), atom2)):
                #     return True
                # if (self.__is_in_list(Not(e), atom1) and self.__is_in_list(e.right, atom2)):
                #     return True
        for e in atom2:
            if (type(e) == Next or (type(e) == Not and type(e.right) == Next)):
                continue
            if (not type(e) == Not and not self.__is_in_list(e, atom1) and not self.__is_in_list(Next(e), atom1)):
                # print("atom2")
                return False
            if (type(e) == Not and not self.__is_in_list(e, atom1) and not self.__is_in_list(Not(Next(Not(e).simplify()[0])), atom1)):
                # print("atom2")
                return False

        return True

    def __get_edge_value(self, atom1, atom2):
        prime = []
        length = len(atom1)
        for i in range(length):
            if atom1[i].get_height() > 2 or type(atom1[i]) is Next:
                break
            if not atom1[i].is_same(atom2[i]):
                prime.append(atom2[i])
        if len(prime) == 0:
            for i in range(length):
                if atom1[i].get_height() > 2 or type(atom1[i]) is Next:
                    break
                if atom1[i].is_same(atom2[i]):
                    prime.append(atom2[i])
        return prime
            

    def gen_buchi(self):
        buchi = Buchi()
        for i in range(len(self.atoms)):
            buchi.add_vertex(i)
            if (self.__atom_is_init(self.atoms[i])):
                buchi.add_init(i)
            if (self.__atom_is_repeated(self.atoms[i])):
                buchi.add_repeated(i)

            for j in range(len(self.atoms)):
                if (self.__atom_has_edge(self.atoms[i], self.atoms[j])):
                    buchi.add_edge([i, j, self.__get_edge_value(self.atoms[i], self.atoms[j])])
        return buchi
