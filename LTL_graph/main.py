from ast import *
import sys

if __name__ == "__main__":
    pass

sys.setrecursionlimit(20000)

line = input("Expression: ")
print(line)

tokens = line.split(" ")

ast = AST()

ast.make_root(tokens)
print(ast.root.to_string())

ast.simplify_root()
print(ast.root.to_string())