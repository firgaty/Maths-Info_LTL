# Expr0 : Var, Top, Bottom
# Expr1 : Next, Eventually, Always, Not
# Expr2 : And, Or, Until, Release

class Expr(object):
    def __init__(self, name, right, left):
        self.name = name
        self.left = left
        self.right = right

    def to_string(self):
        if (type(self.left) == None):
            return "(" + self.name + " " + self.right.to_string() + ")"
        return "(" + self.left.to_string() + " " + self.name + " " + self.right.to_string() + ")"


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


def make_ast(tok_list, left):

    if tok_list == None or len(tok_list) == 0:
        return None, left

    tok = tok_list.pop(0)
    
    if tok == "(":
        return make_ast(tok_list, left)
    if tok == ")":
        return tok_list, left

    if tok == "X":
        tok_list, ast = make_ast(tok_list, None)
        return make_ast(tok_list, Next(ast))
    elif tok == "G":
        tok_list, ast = make_ast(tok_list, None)
        return make_ast(tok_list, Always(ast))
    elif tok == "F":
        tok_list, ast = make_ast(tok_list, None)
        return make_ast(tok_list, Eventually(ast))
    elif tok == "&":
        tok_list, ast = make_ast(tok_list, None)
        return make_ast(tok_list, And(left, ast))
    elif tok == "v":
        tok_list, ast = make_ast(tok_list, None)
        return make_ast(tok_list, Or(left, ast))
    elif tok == "U":
        tok_list, ast = make_ast(tok_list, None)
        return make_ast(tok_list, Until(left, ast))
    elif tok == "not":
        tok_list, ast = make_ast(tok_list, None)
        return make_ast(tok_list, Not(ast))
    elif tok == "true":
        return make_ast(tok_list, Top())
    elif tok == "false":
        return make_ast(tok_list, Bottom())

    return make_ast(tok_list, Var(tok))

def make_top_ast(tok_list):
    tok_list, ast = make_ast(tok_list, None)
    return ast

# TODO simplifications. 

def is_valid_expr0(ast):
    return not (ast == None)

def is_valid_expr1(ast):
    return not (ast == None or ast.right == None)

def is_valid_expr2(ast):
    return not (ast == None or ast.right == None or ast.left == None)

def simpl_not(ast):
    if not is_valid_expr1(ast):
        return ast
    if type(ast.right) == Top:
        return Bottom()
    elif type(ast.right) == Bottom:
        return Top()
    elif type(ast.right) == Not:
        return ast.right.right
    return ast

def simpl_next(ast):
    if not is_valid_expr1(ast):
        return ast
    if type(ast.right) == Top():
        return ast.right
    return ast

def simpl_until(ast):
    if not is_valid_expr2(ast):
        return ast
    if type(ast.right) == Bottom:
        return ast.right
    if type(ast.right) == Next and type(ast.left) == Next:
        return Next(Until(ast.left.right, ast.right.right))

def simplify_ast(ast):
    if type(ast) == Not:
        return simplify_ast(simpl_not(ast))

    if ast.right != None:
        ast.right = simplify_ast(ast.right)
    if ast.left != None:
        ast.left = simplify_ast(ast.left)

    return ast