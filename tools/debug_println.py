#!/usr/bin/env python
"""
Test if println is being parsed correctly
"""
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.lexer import Lexer
from src.core.parser import Parser
from src.core.interpreter import Interpreter

code = 'println("TEST")'

print(f"Code: {code}")
print()

# Tokenize
lex = Lexer(code)
tokens = lex.tokenize()
print("Tokens:")
for t in tokens:
    print(f"  {t}")
print()

# Parse
parser = Parser(tokens)
ast = parser.parse()
print(f"AST: {ast}")
print(f"AST body: {ast.body}")
if ast.body:
    stmt = ast.body[0]
    print(f"  Statement type: {type(stmt).__name__}")
    print(f"  Statement: {stmt}")
    if hasattr(stmt, 'callee'):
        print(f"  Callee: {stmt.callee}")
    if hasattr(stmt, 'args'):
        print(f"  Args: {stmt.args}")
print()

# Evaluate
print("Evaluating...")
interp = Interpreter()
try:
    result = interp.eval(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
