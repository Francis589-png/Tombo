"""
File loader for Tombo `.to` files. Provides `run_file(path, interpreter)` which reads
source, tokenizes, parses and runs it with the given interpreter instance.
"""
import os
from src.core.lexer import Lexer
from src.core.parser import Parser


def run_file(path, interpreter):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    lex = Lexer(src)
    toks = lex.tokenize()
    parser = Parser(toks)
    ast = parser.parse()
    return interpreter.eval(ast)


if __name__ == '__main__':
    # simple runner
    from src.core.interpreter import Interpreter
    interp = Interpreter()
    import sys
    if len(sys.argv) < 2:
        print('Usage: python -m src.core.fs <file.to>')
    else:
        run_file(sys.argv[1], interp)
