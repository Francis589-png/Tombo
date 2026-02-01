#!/usr/bin/env python
"""Debug test."""
import sys
sys.path.insert(0, ".")

from src.lexer import Lexer, TokenType

code = "let change to def defi if else"
lexer = Lexer(code)
tokens = lexer.tokenize()

print("All tokens:")
for i, t in enumerate(tokens):
    print(f"  {i}: {t}")

print("\nFirst token:")
print(f"  Type: {tokens[0].type}")
print(f"  Type == LET: {tokens[0].type == TokenType.LET}")
print(f"  Value: {tokens[0].value}")
