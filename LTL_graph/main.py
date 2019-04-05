from ast import *


if __name__ == "__main__":
    pass

line = input("Expression: ")

tokens = line.split(" ")

tok_list, ast = make_ast(tokens, None)

print(ast.to_string)