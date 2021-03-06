from ast import *
from formulas import *
from graph import *
from gerth import *
import sys

if __name__ == "__main__":
    pass

sys.setrecursionlimit(20000)

explanation = \
    "L'expression attendue est de forme suivante:\
        \n- Toute sous-formule doit être encadrée par des parenthèses\
        \n- Les opérateur sont notés: \
        \n\tOr: v, And: & , Until: U, Release: R\
        \n\tNext: X, Always: G, Eventually: F, Not: !\
        \n- Les variables sont en une seule lettre et les valeurs Bottom(false) Top(true) sont respectivement notées 0 et 1.\
        \nExemple: (((Xa) v b) U ((a R T)))\
        \nQui donnera: ((𝗫a ∨ b) 𝗨 (a 𝗥 T))\n"

exp = True

# # Test
# a = Var("a")
# b = Bottom()

# if type(a) == Var:
#     print("Var")
# if issubclass(a.__class__, Expr0) :
#     print("Expr0")
# # !Test

while (True):

    if exp:
        print(explanation)
        exp = False

    line = input("Expression >>>>>>>>>>>> ")
    # print(line)

    if line == "":
        exp = True
        continue

    # print("Traîtement de l'entrée...")

    tokens = list(line)

    ast = AST()

    ast.make_root(tokens)
    print("AST: \t\t\t" + ast.root.to_string())

    # ast.simplify_root()
    ast.neg_norm_form()
    print("Simplification: \t" + ast.root.to_string())

    g = Gerth(ast.root)
    g.create_graph()

    print(g.to_string())

    gba = g.gba()
    gba.make_dot()


    # formulas = Formula(ast.root)
    # print("Sous-formules: \t\t" + formulas.to_string())
    # print("Sous-formules neg: \t" + formulas.to_string(1))

    # formulas.gen_atoms()
    # print("Atomes: " + str(len(formulas.atoms)))
    # print(formulas.to_string(2))

    # buchi = formulas.gen_buchi()
    # print(buchi)

    # buchi.make_dot(formulas.get_atoms(), formulas.ast)
