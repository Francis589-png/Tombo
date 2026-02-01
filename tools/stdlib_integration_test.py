"""
Simple test to verify library functions work with .to files
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.interpreter import Interpreter
from src.core.lexer import Lexer
from src.core.parser import Parser

code = """
# Test core functions
let x = int("42")
println(x)

# Test math
let root = sqrt(16)
println(root)

# Test string
let msg = upper("hello")
println(msg)

# Test collections
let arr = [5, 3, 8, 1]
sort(arr)
println(arr)

# Test type conversion
let s = str(123)
println(s)
"""

print("=" * 60)
print("TOMBO STDLIB INTEGRATION TEST")
print("=" * 60)
print()

interp = Interpreter()
lex = Lexer(code)
tokens = lex.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print("Executing code:")
print("-" * 60)
interp.eval(ast)
print("-" * 60)
print()
print("=" * 60)
print("TEST COMPLETED SUCCESSFULLY ✓")
print("=" * 60)
