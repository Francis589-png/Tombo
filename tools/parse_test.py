import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.core.lexer import Lexer
from src.core.parser import Parser

code = '''
let x = 5
def add_one(n)
    return n + 1
end

let arr = [1, 2, 3]
let y = add_one(4)
'''

lex = Lexer(code)
tokens = lex.tokenize()
print('TOKENS:')
for t in tokens:
    print(f"  {t}")
print('\nAST:')
parser = Parser(tokens)
ast = parser.parse()
print(ast)
