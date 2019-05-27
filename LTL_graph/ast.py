# Expr0 : Var, Top, Bottom
# Expr1 : Next, Eventually, Always, Not
# Expr2 : And, Or, Until, Release


class Expr(object):
    def __init__(self, name, right, left):
        self.name = name
        self.left = left
        self.right = right
        self.formula = None
        self.height = None
        self.logic_height = None

    def to_string(self):
        if (type(self.left) == None):
            return "(" + self.name + " " + self.right.to_string() + ")"
        return "(" + self.left.to_string() + " " + self.name + " " + self.right.to_string() + ")"

    def is_valid_expr(self):
        return not (self.right == None or self.left == None)

    def is_same(self, expr):
        if (self.name != expr.name):
            return False
        if (type(self) == Bottom or type(self) == Top or type(self) == Var):
            return True
        return (self.left.is_same(expr.left) if self.left != None and expr.left != None else True) and self.right.is_same(expr.right)

    def contains(self, expr):
        return self.is_same(expr) or (self.left.contains(expr) if self.left != None else False) or (self.right.contains(expr) if self.right != None else False)
        
    def simplify(self):
        return self, False

    def __simplify(self):
        return self, False

    def get_height(self, force=False):
        if(self.height is None or force):
            self.height = 1 + max(self.left.get_height(force), self.right.get_height(force))
        return self.height

    def get_logic_height(self, force=False):
        if(self.height is None or force):
            self.height = 1 + max(self.left.get_logic_height(force), self.right.get_logic_height(force))
        return self.height

class Expr0(Expr):
    def __init__(self, name):
        super(Expr0, self).__init__(name, None, None)

    def to_string(self):
        return self.name

    def is_valid_expr(self):
        return not self.name == None

    def get_height(self, force=False):
        return 1

    def get_logic_height(self, force=False):
        return 1

class Expr1(Expr):
    def __init__(self, name, right):
        super(Expr1, self).__init__(name, right, None)


    def to_string(self):
        # return "(" + self.name + self.right.to_string() + ")"
        return self.name + self.right.to_string()

    def is_valid_expr(self):
        return not self.right == None
    
    def get_height(self, force=False):
        if(self.height is None or force):
            self.height = 1 + self.right.get_height(force)
        return self.height
    
    def get_logic_height(self, force=False):
        if(self.logic_height is None or force):
            self.logic_height = 1 + self.right.get_logic_height(force)
        return self.logic_height

class Expr2(Expr):
    def __init__(self, name, left, right):
        super(Expr2, self).__init__(name, right, left)


class Top(Expr0):
    def __init__(self):
        super(Top, self).__init__("⊤")


class Bottom(Expr0):
    def __init__(self):
        super(Bottom, self).__init__("⊥")


class Var(Expr0):
    def __init__(self, name):
        super(Var, self).__init__(name)


class Not(Expr1):
    def __init__(self, right):
        super(Not,self).__init__("¬", right)

    def simplify(self):
        if not self.is_valid_expr():
            return self, False
        if type(self.right) == Top:
            return Bottom(), True
        elif type(self.right) == Bottom:
            return Top(), True
        elif type(self.right) == Not:
            return self.right.right, True
        return self, False

class Next(Expr1):
    def __init__(self, right):
        super(Next, self).__init__("𝗫", right)

    def simplify(self):
        if not self.is_valid_expr():
            return self, False
        if type(self.right) == Top or type(self.right) == False: 
            return self.right, True
        if type(self.right) == Always and type(self.right.right) == Eventually:
            return self.right, True
        return self, False

    def get_logic_height(self, force=False):
        return 1

class Eventually(Expr1):
    def __init__(self, right):
        super(Eventually, self).__init__("𝗙", right)

    def simplify(self):
        if not self.is_valid_expr():
            return self, False
        return Until(Top(), self.right), False
        # return self, False

class Always(Expr1):
    def __init__(self, right):
        super(Always, self).__init__("𝗚", right)


    def simplify(self):
        if not self.is_valid_expr():
            return self, False
        if (type(self.right) == Release):
            self.right.left = Bottom()
            return self.right, True
        return Release(Bottom(), self.right), True
        # return self, False

class And(Expr2):
    def __init__(self, left, right):
        super(And, self).__init__("∧", left, right)

    def simplify(self):
        if not self.is_valid_expr():
            return self, False
        if type(self.left) == Top and type(self.right) == Top:
            return Top(), True
        if type(self.right) == Until or type(self.right) == Release:
            if self.left.is_same(self.right.right):
                return self.left, True
        if type(self.right) == Next and type(self.left) == Next:
            return Next(And(self.left.right, self.right.right)), True
        if self.right.contains(self.left):
            return self.right, True
        if self.left.contains(self.right):
            return self.left, True
        return Or((Not(self.left)), (Not(self.right))), True  # transformation en Ou


class Or(Expr2):
    def __init__(self, left, right):
        super(Or, self).__init__("∨", left, right)

    def simplify(self):
        # TODO finir a v !a, a v a
        if not self.is_valid_expr():
            return self, False
        if type(self.left) == Top or type(self.right) == Top:
            return Top(), True            
        if self.left.is_same(self.right):
            return self.left, True
        if type(self.left) == Always and type(self.right) == Always and type(self.left.right) == Eventually and type(self.right.right) == Eventually:
            return Always(Eventually(Or(self.left.right, self.right.right))), True
        if type(self.left) == Release and type(self.right) == Release and self.left.right.is_same(self.right.right):
            return Release(Or(self.left.left, self.right.left), self.right.right), True
        if self.right.contains(Not(self.left)) or self.left.contains(Not(self.right)):
            return Top(), True
        return self, False

class Until(Expr2):
    def __init__(self, left, right):
        super(Until, self).__init__("𝗨", left, right)

    def simplify(self):
        if not self.is_valid_expr():
            return self, False
        if type(self.right) == Bottom or type(self.right) == Top:
            return self.right, True
        if type(self.right) == Next and type(self.left) == Next:
            return Next(Until(self.left.right, self.right.right)), True
        if self.right.contains(self.left):
            return self.right, True
        if type(self.right) == Until and self.right.left.contains(self.left):
            return self.right, True
        return self, False  


class Release(Expr2):
    def __init__(self, left, right):
        super(Release, self).__init__("𝗥", left, right)

    def simplify(self):
        if not self.is_valid_expr():
            return self, False
        return Not(Until(Not(self.left).simplify()[0], Not(self.right).simplify()[0])), True
        # return self, False

class AST(object):
    def __init__(self):
        self.root = None
        self.height = 0

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
        elif tok == "1":
            return self.__make_ast(tok_list, Top())
        elif tok == "0":
            return self.__make_ast(tok_list, Bottom())

        return self.__make_ast(tok_list, Var(tok))

    def make_root(self, tok_list):
        tok_list, ast = self.__make_ast(tok_list, None)
        self.root = ast    

    @staticmethod
    def simplify_ast(ast):
        while True:
            changed, changed_l, changed_r = False, False, False
            while True:
                ast, changed = ast.simplify()
                if not changed:
                    break

            if ast.right != None:
                while True:
                    ast.right, changed_r = AST.simplify_ast(ast.right)
                    if not changed_r:
                        break

            if ast.left != None:
                while True:
                    ast.left, changed_l = AST.simplify_ast(ast.left)
                    if not changed_l:
                        break
            if not (changed or changed_l or changed_r):
                return ast, False

    def simplify_root(self):
        self.root = self.simplify_ast(self.root)[0]

######################
#       Autres       #
######################
        
        
