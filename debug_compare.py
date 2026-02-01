import sys
sys.path.insert(0, 'C:/Users/FRANCIS JUSU/Documents/TOMBO/src')
from lexer.lexer import Lexer
from lexer.token_types import TokenType
code = 'let d = 10\n'
lexer = Lexer(code)
tokens = lexer.tokenize()
print(tokens[0].type, TokenType.LET)
print('eq:', tokens[0].type == TokenType.LET)
print('in check:', tokens[0].type in (TokenType.LET,))
