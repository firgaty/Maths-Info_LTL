from ast import *


if __name__ == "__main__":
    pass

line = input("Expression: ")

tokens = line.split(" ")

ast = make_top_ast(tokens)
print(ast.to_string())

ast = simplify_ast(ast)
print(ast.to_string())