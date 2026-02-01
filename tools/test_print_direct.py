"""
Direct test - print and verify output
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Starting test...")
sys.stdout.flush()

from src.core.interpreter import Interpreter
from src.core.lexer import Lexer
from src.core.parser import Parser

code = """
print("TEST: 42")
"""

interp = Interpreter()
lex = Lexer(code)
tokens = lex.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print("About to evaluate...")
sys.stdout.flush()

interp.eval(ast)

print("After evaluation")
sys.stdout.flush()
