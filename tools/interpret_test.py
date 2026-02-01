import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.core.lexer import Lexer
from src.core.parser import Parser
from src.core.interpreter import Interpreter

code = '''
let x = 5
def add_one(n)
    return n + 1
end

let arr = [1, 2, 3]
let y = add_one(4)
'''
lex = Lexer(code)
toks = lex.tokenize()
parser = Parser(toks)
ast = parser.parse()
interp = Interpreter()
interp.eval(ast)
print('GLOBAL ENV:')
for k,v in interp.global_env.store.items():
    print(' ', k, '->', v)
fn = interp.global_env.get('add_one')
if fn:
    print('add_one(2)=', fn.call([2], interp))
