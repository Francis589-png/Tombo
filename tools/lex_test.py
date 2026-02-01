import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.core.lexer import Lexer

code = '''
let x = 5
if x > 0
    change x to 10
    defi add(a, b) => a + b
end
'''

lexer = Lexer(code)
toks = lexer.tokenize()
for t in toks:
    print(f"{t.line}:{t.col}  {t.type.name}  {t.value}")
