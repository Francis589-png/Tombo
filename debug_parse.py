import sys
sys.path.insert(0, 'C:/Users/FRANCIS JUSU/Documents/TOMBO/src')
from lexer.lexer import Lexer
from parser.parser import Parser
code = 'let d = 10\n'
lexer = Lexer(code)
tokens = lexer.tokenize()
print('TOKENS:', tokens)
parser = Parser(tokens)
ast = parser.parse()
print('AST:', ast)
