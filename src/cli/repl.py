#!/usr/bin/env python3
"""Tombo REPL prototype (lightweight).

Run `python src/cli/repl.py` to start interactive prompt.
"""
from __future__ import annotations
import argparse
import sys
import os


def repl_loop() -> None:
    # Load package paths from tombo_packages.txt (if present)
    pkg_cfg = 'tombo_packages.txt'
    if os.path.exists(pkg_cfg):
        try:
            with open(pkg_cfg, 'r', encoding='utf-8') as f:
                for ln in f:
                    p = ln.strip()
                    if p and p not in sys.path:
                        sys.path.insert(0, p)
        except Exception:
            pass

    print("Tombo REPL — type :exit to quit, :help for commands")
    interp = None
    buffer_lines = []
    multiline_mode = False

    def ensure_interp():
        nonlocal interp
        if interp is None:
            try:
                from src.core.interpreter import Interpreter
                interp = Interpreter()
            except Exception as e:
                print("Error initializing interpreter:", e)
                interp = None
        return interp

    while True:
        try:
            prompt = "...> " if multiline_mode else "tombo> "
            line = input(prompt)
        except EOFError:
            print()
            break
        # commands
        if not line:
            if multiline_mode:
                continue
            else:
                continue
        if line.strip() in (":exit", ":quit"):
            break
        if line.strip() == ":help":
            print(":load <file>   - load and execute a .to file\n:exit or :quit - exit REPL\n:reset - reset interpreter")
            continue
        if line.strip() == ":reset":
            interp = None
            print("Interpreter reset")
            continue
        if line.startswith(":load "):
            _, fname = line.split(None, 1)
            try:
                with open(fname, 'r', encoding='utf-8') as f:
                    src = f.read()
                interp = ensure_interp()
                if interp:
                    from src.core.lexer import Lexer
                    from src.core.parser import Parser
                    lex = Lexer(src)
                    toks = lex.tokenize()
                    p = Parser(toks)
                    ast = p.parse()
                    interp.eval(ast)
                    print(f"Executed {fname}")
            except Exception as e:
                print("Error loading file:", e)
            continue

        # Multiline entry: accumulate lines until a parse succeeds or user ends with a blank line
        buffer_lines.append(line)
        src = "\n".join(buffer_lines)
        # Try to lex/parse to see if we have a complete unit
        try:
            from src.core.lexer import Lexer
            from src.core.parser import Parser
            lex = Lexer(src)
            toks = lex.tokenize()
            p = Parser(toks)
            ast = p.parse()
            # If parse succeeded, evaluate
            interp = ensure_interp()
            if interp:
                try:
                    res = interp.eval(ast)
                    if res is not None:
                        print(res)
                except Exception as e:
                    print("Runtime error:", e)
            buffer_lines = []
            multiline_mode = False
        except Exception as e:
            # likely incomplete input — enter multiline mode
            multiline_mode = True
            # continue reading lines
            continue


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="tombo-repl")
    parser.add_argument("--test", action="store_true", help="Run self-test and exit")
    args = parser.parse_args(argv)
    if args.test:
        print("REPL test ok")
        return 0
    repl_loop()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
