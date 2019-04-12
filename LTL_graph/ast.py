# Expr0 : Var, Top, Bottom
# Expr1 : Next, Eventually, Always, Not
# Expr2 : And, Or, Until, Release

class Expr(object):
    def __init__(self, name, right, left):
        self.name = name
        self.left = left
        self.right = right
        self.formula = None

    def to_string(self):
        if (type(self.left) == None):
            return "(" + self.name + " " + self.right.to_string() + ")"
        return "(" + self.left.to_string() + " " + self.name + " " + self.right.to_string() + ")"

    def is_valid_expr0(self):
        return not self.name == None

    def is_valid_expr1(self):
        return not self.right == None

    def is_valid_expr2(self):
        return not (self.right == None or self.left == None)


class Expr0(Expr):
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

    def to_string(self):
        return self.name


class Expr1(Expr):
    def __init__(self, name, right):
        self.name = name
        self.left = None
        self.right = right

    def to_string(self):
        return "(" + self.name + " " + self.right.to_string() + ")"


class Expr2(Expr):
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right


class Top(Expr0):
    def __init__(self):
        self.name = "true"
        self.left = None
        self.right = None


class Bottom(Expr0):
    def __init__(self):
        self.name = "false"
        self.left = None
        self.right = None


class Var(Expr0):
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class Not(Expr1):
    def __init__(self, right):
        self.name = "not"
        self.right = right
        self.left = None


class Next(Expr1):
    def __init__(self, right):
        self.name = "next"
        self.right = right
        self.left = None


class Eventually(Expr1):
    def __init__(self, right):
        self.name = "eventually"
        self.right = right
        self.left = None


class Always(Expr1):
    def __init__(self, right):
        self.name = "always"
        self.right = right
        self.left = None


class And(Expr2):
    def __init__(self, left, right):
        self.name = "and"
        self.left = left
        self.right = right


class Or(Expr2):
    def __init__(self, left, right):
        self.name = "or"
        self.left = left
        self.right = right


class Until(Expr2):
    def __init__(self, left, right):
        self.name = "until"
        self.left = left
        self.right = right


class Release(Expr2):
    def __init__(self, left, right):
        self.name = "release"
        self.left = left
        self.right = right


class AST(object):
    def __init__(self):
        self.root = None
        self.sub_formula_table = []
        self.sub_formula_index = {}

    def __make_ast(self, tok_list, left):
        if tok_list == None or len(tok_list) == 0:
            return None, left

        tok = tok_list.pop(0)

        if tok == "(":
            return self.__make_ast(tok_list, left)
        if tok == ")":
            return tok_list, left

        if tok == "X":
            tok_list, ast = self.__make_ast(tok_list, None)
            return self.__make_ast(tok_list, Next(ast))
        elif tok == "G":
            tok_list, ast = self.__make_ast(tok_list, None)
            return self.__make_ast(tok_list, Always(ast))
        elif tok == "F":
            tok_list, ast = self.__make_ast(tok_list, None)
            return self.__make_ast(tok_list, Eventually(ast))
        elif tok == "&":
            tok_list, ast = self.__make_ast(tok_list, None)
            return self.__make_ast(tok_list, And(left, ast))
        elif tok == "v":
            tok_list, ast = self.__make_ast(tok_list, None)
            return self.__make_ast(tok_list, Or(left, ast))
        elif tok == "U":
            tok_list, ast = self.__make_ast(tok_list, None)
            return self.__make_ast(tok_list, Until(left, ast))
        elif tok == "not":
            tok_list, ast = self.__make_ast(tok_list, None)
            return self.__make_ast(tok_list, Not(ast))
        elif tok == "true":
            return self.__make_ast(tok_list, Top())
        elif tok == "false":
            return self.__make_ast(tok_list, Bottom())

        return self.__make_ast(tok_list, Var(tok))

    def make_root(self, tok_list):
        tok_list, ast = self.__make_ast(tok_list, None)
        self.root = ast

    def _simpl_not(self, ast):
        if not ast.is_valid_expr1():
            return ast
        if type(ast.right) == Top:
            return Bottom()
        elif type(ast.right) == Bottom:
            return Top()
        elif type(ast.right) == Not:
            return ast.right.right
        return ast

    def _simpl_next(self, ast):
        if not ast.is_valid_expr1():
            return ast
        if type(ast.right) == Top():
            return ast.right
        return ast

    def _simpl_until(self, ast):
        if not ast.is_valid_expr2():
            return ast
        if type(ast.right) == Bottom:
            return ast.right
        if type(ast.right) == Next and type(ast.left) == Next:
            return Next(Until(ast.left.right, ast.right.right))

    def _simpl_and(self, ast):
        if not ast.is_valid_expr2():
            return ast
        if type(ast.right) == Next and type(ast.left) == Next:
            return Next(And(ast.left.right, ast.right.right))
        return Or(Not(ast.left), Not(ast.left)) # transformation en Ou

    # TODO
    def _simpl_or(self, ast):
        return ast

    # TODO
    def _simpl_always(self, ast):
        return ast

    # TODO
    def _simplify_always(self, ast):
        return ast

    # TODO
    def _simpl_release(self, ast):
        return ast

    def _simplify_ast(self, ast):
        # TODO optimiser récursif.

        if type(ast) == Not:
            return self._simplify_ast(self._simpl_not(ast))
        # elif type(ast) == Eventually:
        #     return self._simplify_ast(self._simplify_always(ast))
        # elif type(ast) == Or:
        #     return self._simplify_ast(self._simpl_or(ast))
        # elif type(ast) == And:
        #     return self._simplify_ast(self._simpl_and(ast))
        # elif type(ast) == Until:
        #     return self._simplify_ast(self._simpl_until(ast))
        # elif type(ast) == Release:
        #     return self._simplify_ast(self._simpl_release(ast))
        # elif type(ast) == Always:
        #     return self._simplify_ast(self._simpl_always(ast))
        # elif type(ast) == Next:
        #     return self._simplify_ast(self._simpl_next(ast))

        if ast.right != None:
            ast.right = self._simplify_ast(ast.right)
        if ast.left != None:
            ast.left = self._simplify_ast(ast.left)

        return ast

    def simplify_root(self):
        self.root = self._simplify_ast(self.root)

    def _add_formula(self, formula, ast):
        if formula in self.sub_formula_index:
            return self.sub_formula_index[formula]
        self.sub_formula_index[formula] = len(self.sub_formula_table)
        self.sub_formula_table.append(ast)
        self.sub_formula_index["(not " + formula + ")"] = len(self.sub_formula_table)
        self.sub_formula_table.append(Not(ast))

    # Merci Python de ne pas faire de récursion terminale, merci Guido. /s
    def _gen_formulas(self, ast):
        node = [(ast, 0)] # stack
        right = None
        left = [] # stack

        while node[-1] != None:
            if node[-1][0].left != None and node[-1][1] < 1:
                node.append((node[-1][0].left, 1))
                continue
            if node[-1][0].right != None and node[-1][1] < 2:
                node.append((node[-1][0].right, 2))
                continue

            if node[-1][0].left == None and node[-1][0].right == None:
                # TODO
                return

    def gen_formulas(self):
        self._gen_formulas(self.root)
        return

######################
#   Simplification   #
######################

# TODO simplifications. 



######################
#       Atomes       #
######################