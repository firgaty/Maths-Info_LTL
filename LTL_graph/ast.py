class Expr:
    def __init__(self, name, right, left):
        self.name = name
        self.left = left
        self.right = right

    def to_string(self):
        return "(" + self.left.to_string() + " " + self.name +" " + self.right.to_string() + ")"

class Expr0(Expr):
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

    def to_string(self):
        return self.name 

class Expr1(Expr):
    def __init__(self, name, right) :
        self.name = name
        self.left = None
        self.right = right

    def to_string(self):
        return self.name + " " + self.left.to_string()

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
    def __init__(self, right) :
        self.name = "not"
        self.right = right

class Next(Expr1):
    def __init__(self, right) :
        self.name = "next"
        self.right = right

class Eventually(Expr1):
    def __init__(self, right) :
        self.name = "eventually"
        self.right = right

class Always(Expr1):
    def __init__(self, right) :
        self.name = "always"
        self.right = right

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

    if (len(tok_list) == 0):
        return left

    tok = tok_list.pop(0)

    # pas bon : copie de listes
    
    if tok == "(":
        return make_ast(tok_list, left)
    if tok == ")":
        return tok_list, left

    if tok == "X":
        tok_list, ast = make_ast(tok_list, None)
        return make_ast(tok_list, Next(ast))
    elif tok == "G":
        tok_list, ast = make_ast(tok_list, None)
        return tok_list, Always(ast)
    elif tok == "F":
        tok_list, ast = make_ast(tok_list, None)
        return tok_list, Eventually(ast)
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
        return tok_list, Eventually(ast)
    elif tok == "true":
        return make_ast(tok_list, Top())
    elif tok == "false":
        return make_ast(tok_list, Bottom())
    
    return make_ast(tok_list, Var(tok))
