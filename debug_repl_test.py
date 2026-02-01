import sys
sys.path.insert(0, 'C:/Users/FRANCIS JUSU/Documents/TOMBO/src')
from lexer.lexer import Lexer
from parser.parser import Parser

code = 'for i in [1,2,3,]\nprintln(i)\nend\n'
lexer = Lexer(code)
tokens = lexer.tokenize()
print('Tokens:', [(t.type.name, t.value) for t in tokens if t.type.name not in ('NEWLINE','INDENT','DEDENT','EOF')])
parser = Parser(tokens)
ast = parser.parse()
print('Parsed AST statements count:', len(ast.statements))
print('First stmt type:', type(ast.statements[0]).__name__ if ast.statements else None)
