import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.core.lexer import Lexer
from src.core.parser import Parser
from src.core.interpreter import Interpreter
from src.core.domain import DomainManager

# Ensure domain manager exists
dm = DomainManager.get()

code = '''
use web
let s = server(8000)
'''
lex = Lexer(code)
toks = lex.tokenize()
parser = Parser(toks)
ast = parser.parse()
interp = Interpreter()
interp.eval(ast)
print('ENV:')
for k,v in interp.global_env.store.items():
    print(' ', k, '->', v)
