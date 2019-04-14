from ast import *
import sys

if __name__ == "__main__":
    pass

sys.setrecursionlimit(20000)

explanation = \
    "L'expression attendue est de forme suivante:\
        \n- Toute sous-formule doit être encadrée par des parenthèses\
        \n- Les opérateur sont notés: \
        \n\tOr: v, And: & , Until: U, Release: R\
        \n\tNext: X, Always: G, Eventually: F\
        \n- Les variables sont en une seule lettre et les valeurs Bottom(false) Top(true) sont respectivement notées B et T (notez la majuscule).\
        \nExemple: (((Xa) v b) U ((a R T)))\
        \nQui donnera: (((next a) or b) until (a release true))\n"

exp = True

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
    print("AST: \t\t\t"+ ast.root.to_string())

    ast.simplify_root()
    print("Simplification: \t"+ ast.root.to_string())

    formulas = ast.gen_formulas()
    print("Sous-formules: \t\t" + formulas.to_string())
