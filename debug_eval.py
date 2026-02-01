import sys
sys.path.insert(0, 'C:/Users/FRANCIS JUSU/Documents/TOMBO/src')
from lexer.lexer import Lexer
from parser.parser import Parser
from core.interpreter import Interpreter
code = 'let d = 10\nprintln(d)\n'
lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
print('AST parsed:', ast)
interp = Interpreter()
res = interp.eval(ast)
print('Result:', res)
