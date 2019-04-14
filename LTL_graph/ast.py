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

    def is_same(self, expr):
        if (self.name != expr.name):
            return False
        if (type(self) == Bottom or type(self) == Top or type(self) == Var):
            return True
        return (self.left.is_same(expr.left) if self.left != None and expr.left != None else True) and self.right.is_same(expr.right)

    def contains(self, expr):
        return self.is_same(expr) or (self.left.contains(expr) if self.left != None else False) or (self.right.contains(expr) if self.right != None else False)


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


class Formula(object):
    def __init__(self):
        self.f_list = []

    # check si la formule ou la negation de la formule est déjà dans
    # la liste des sous formules
    def __is_in_list(self, ast):
        for l in self.f_list:
            if l.is_same(ast) or l.is_same(Not(ast)):
                return True
        return False

    def add(self, ast):
        if (self.__is_in_list(ast)):
            return False
        self.f_list.append(ast)
        return True

    def to_string(self):
        s = "[|"
        for l in self.f_list:
            s += " " + l.to_string() + " |"
        s += "]"
        return s


class AST(object):
    def __init__(self):
        self.root = None

    def __make_ast(self, tok_list, left):
        if tok_list == None or len(tok_list) == 0:
            return None, left

        tok = tok_list.pop(0)

        if tok == "(" or tok == " ":
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
        elif tok == "R":
            tok_list, ast = self.__make_ast(tok_list, None)
            return self.__make_ast(tok_list, Release(left, ast))
        elif tok == "!":
            tok_list, ast = self.__make_ast(tok_list, None)
            return self.__make_ast(tok_list, Not(ast))
        elif tok == "T":
            return self.__make_ast(tok_list, Top())
        elif tok == "B":
            return self.__make_ast(tok_list, Bottom())

        return self.__make_ast(tok_list, Var(tok))

    def make_root(self, tok_list):
        tok_list, ast = self.__make_ast(tok_list, None)
        self.root = ast

######################
#   Simplification   #
######################

    def __simple_not(self, ast):
        if not ast.is_valid_expr1():
            return ast, False
        if type(ast.right) == Top:
            return Bottom(), True
        elif type(ast.right) == Bottom:
            return Top(), True
        elif type(ast.right) == Not:
            return ast.right.right, True
        return ast, False

    def __simple_next(self, ast):
        if not ast.is_valid_expr1():
            return ast, False
        if type(ast.right) == Top:
            return ast.right, True
        if type(ast.right) == Always and type(ast.right.right) == Eventually:
            return ast.right, True
        return ast, False

    def __simple_until(self, ast):
        if not ast.is_valid_expr2():
            return ast, False
        if type(ast.right) == Bottom:
            return ast.right, True
        if type(ast.right) == Next and type(ast.left) == Next:
            return Next(Until(ast.left.right, ast.right.right)), True
        if ast.right.contains(ast.left):
            return ast.right, True
        if type(ast.right) == Until and ast.right.left.contains(ast.left):
            return ast.right, True
        return ast, False

    def __simple_and(self, ast):
        if not ast.is_valid_expr2():
            return ast, False
        if type(ast.right) == Until or type(ast.right) == Release:
            if ast.left.is_same(ast.right.right):
                return ast.left, True
        if type(ast.right) == Next and type(ast.left) == Next:
            return Next(And(ast.left.right, ast.right.right)), True
        if ast.right.contains(ast.left):
            return ast.right, True
        if ast.left.contains(ast.right):
            return ast.left, True
        return Or(Not(ast.left), Not(ast.right)), True  # transformation en Ou

    # TODO
    def __simple_or(self, ast):
        if not ast.is_valid_expr2():
            return ast, False
        if type(ast.left) == Always and type(ast.right) == Always and type(ast.left.right) == Eventually and type(ast.right.right) == Eventually:
            return Always(Eventually(Or(ast.left.right, ast.right.right))), True
        if type(ast.left) == Release and type(ast.right) == Release and ast.left.right.is_same(ast.right.right):
            return Release(Or(ast.left.left, ast.right.left), ast.right.right), True
        if ast.right.contains(Not(ast.left)) or ast.left.contains(Not(ast.right)):
            return Top(), True
        return ast, False

    # TODO
    def __simple_always(self, ast):
        if not ast.is_valid_expr1():
            return ast, False
        if (type(ast.right) == Release):
            ast.right.left = Bottom()
            return ast.right, True
        return Release(Bottom(), ast.right), True
        # return ast, False

    # TODO
    def __simple_eventually(self, ast):
        if not ast.is_valid_expr1():
            return ast, False
        return Until(Top(), ast.right), False
        # return ast, False

    # TODO
    def __simple_release(self, ast):
        if not ast.is_valid_expr2():
            return ast, False
        return Not(Until(Not(ast.left), Not(ast.right))), True
        # return ast, False

    def simplify_ast(self, ast):
        # TODO optimiser récursif.

        changed, changed_r, changed_l = False, False, False
        if type(ast) == Not:
            ast, changed = self.__simple_not(ast)
        elif type(ast) == Eventually:
            ast, changed = self.__simple_eventually(ast)
        elif type(ast) == Or:
            ast, changed = self.__simple_or(ast)
        elif type(ast) == And:
            ast, changed = self.__simple_and(ast)
        elif type(ast) == Until:
            ast, changed = self.__simple_until(ast)
        elif type(ast) == Release:
            ast, changed = self.__simple_release(ast)
        elif type(ast) == Always:
            ast, changed = self.__simple_always(ast)
        elif type(ast) == Next:
            ast, changed = self.__simple_next(ast)

        if changed:
            self.simplify_ast(ast)

        if ast.right != None:
            ast.right, changed_r = self.simplify_ast(ast.right)
            if changed:
                ast, changed = self.simplify_ast(ast)
        if ast.left != None:
            ast.left, changed_l = self.simplify_ast(ast.left)
            if changed:
                ast, changed = self.simplify_ast(ast)

        return ast, changed or changed_l or changed_r

    def simplify_root(self):
        self.root, changed = self.simplify_ast(self.root)

######################
#       Atomes       #
######################

    def __gen_formulas(self, formulas, ast):
        formulas.add(ast)
        if ast.left != None:
            self.__gen_formulas(formulas, ast.left)
        if ast.right != None:
            self.__gen_formulas(formulas, ast.right)

    def gen_formulas(self):
        formulas = Formula()
        self.__gen_formulas(formulas, self.root)
        return formulas
