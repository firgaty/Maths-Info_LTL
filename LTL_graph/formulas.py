from ast import *
import itertools

class Formula(object):
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
        # if type(ast) == Top or type(ast) == Bottom:
        #     return True
        if type(ast) == Not:
            ast = ast.right
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

    def to_string(self, list_type=0):
        s = "[|"
        if list_type == 0:
            for l in self.posf_list:
                s += " " + l.to_string() + " |"
        elif list_type == 1:
            for l in self.negf_list:
                s += " " + l.to_string() + " |"
        elif list_type == 2:
            s += "\n"
            for l in self.atoms:
                s += "{|"
                for e in l:
                    s += " " + e.to_string() + " |"
                s += "},\n"
        s += "]"
        return s

    def sort_pos(self):
        # Tri les variables et les Next devant.
        self.posf_list.sort(key=lambda x: x.get_logic_height(True), reverse=False)
        i = 0
        while self.posf_list[i].get_logic_height() == 1:
            i += 1
        self.pos_1 = i
        # Tri des variables devant les Next.
        self.posf_list[0:i] = sorted(self.posf_list[0:i], key=lambda x: x.get_height(True), reverse=False)
    
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
                or ((type(ast.left) == Top or self.__is_in_list(ast.left, atom)) \
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
        for values in itertools.product([True,False],repeat=self.pos_1):
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