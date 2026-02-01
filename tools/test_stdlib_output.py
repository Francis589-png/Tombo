#!/usr/bin/env python
"""
Test stdlib loading with explicit output
"""
import sys
import os

# Unbuffered output
sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

print(f"Project root: {project_root}")

from src.core.interpreter import Interpreter
from src.core.lexer import Lexer
from src.core.parser import Parser

print("Interpreter imported successfully")

code = """
println("Hello from Tombo!")
let x = 42
println(x)
"""

interp = Interpreter()
print(f"Interpreter created with {len(interp.global_env.store)} builtin functions")

lex = Lexer(code)
tokens = lex.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print("Running Tombo code...")
print("-" * 40)
interp.eval(ast)
print("-" * 40)
print("Done!")
