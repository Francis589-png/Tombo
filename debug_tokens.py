import sys
sys.path.insert(0, 'C:/Users/FRANCIS JUSU/Documents/TOMBO/src')
from lexer.lexer import Lexer
code = 'let d = 10\n'
lexer = Lexer(code)
tokens = lexer.tokenize()
for t in tokens:
    print(repr(t))
