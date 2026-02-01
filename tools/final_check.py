#!/usr/bin/env python3
"""Quick end-to-end test of Tombo interpreter"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.core.lexer import Lexer
from src.core.parser import Parser
from src.core.interpreter import Interpreter

# Test 1: Basic arithmetic
code1 = """let x = 2
let y = 3
let z = x + y
"""

print("Test 1: Basic arithmetic")
lex = Lexer(code1)
toks = lex.tokenize()
p = Parser(toks)
ast = p.parse()
i = Interpreter()
i.eval(ast)
print(f"  z = {i.global_env.get('z')} (expected: 5)")
assert i.global_env.get('z') == 5

# Test 2: String function
code2 = """let text = "hello"
let upper_text = upper(text)
"""

print("Test 2: String function (stdlib)")
lex = Lexer(code2)
toks = lex.tokenize()
p = Parser(toks)
ast = p.parse()
i = Interpreter()
i.eval(ast)
result = i.global_env.get('upper_text')
print(f"  upper('hello') = {result} (expected: HELLO)")
assert result == "HELLO"

# Test 3: Function definition
code3 = """defi multiply(a, b) => a * b
let result = multiply(6, 7)
"""

print("Test 3: Function definition and call")
lex = Lexer(code3)
toks = lex.tokenize()
p = Parser(toks)
ast = p.parse()
i = Interpreter()
i.eval(ast)
result = i.global_env.get('result')
print(f"  multiply(6, 7) = {result} (expected: 42)")
assert result == 42

print("\nAll tests PASSED ✓")
