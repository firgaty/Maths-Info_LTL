from ast import *


if __name__ == "__main__":
    pass

line = input("Expression: ")

tokens = line.split(" ")

ast = AST()

ast.make_root(tokens)
print(ast.root.to_string())

ast.simplify_root()
print(ast.root.to_string())