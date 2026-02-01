#!/usr/bin/env python
"""Debug operators test."""
import sys
sys.path.insert(0, ".")

from src.lexer import Lexer, TokenType

code = "+ - * / = == !="
lexer = Lexer(code)
tokens = lexer.tokenize()

print("All tokens:")
for i, t in enumerate(tokens):
    if t.type not in (TokenType.NEWLINE, TokenType.EOF):
        print(f"  {i}: {t}")

print("\nExpected types:")
print(f"  tokens[0] == PLUS: {tokens[0].type == TokenType.PLUS}")
print(f"  tokens[2] == MINUS: {tokens[2].type == TokenType.MINUS}")
print(f"  tokens[6] == EQEQ: {tokens[6].type == TokenType.EQEQ}")
