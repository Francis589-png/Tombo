"""
Debug test - check if print is working
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.interpreter import Interpreter
from src.core.lexer import Lexer
from src.core.parser import Parser

code = """
print("HELLO FROM TOMBO")
"""

print("Creating interpreter...")
interp = Interpreter()

print("Checking print function:")
print_fn = interp.global_env.get('print')
print(f"  print function: {print_fn}")

print("\nParsing code...")
lex = Lexer(code)
tokens = lex.tokenize()
print(f"  Tokens: {len(tokens)}")

parser = Parser(tokens)
ast = parser.parse()
print(f"  AST created")

print("\nEvaluating...")
interp.eval(ast)

print("\nDone!")
