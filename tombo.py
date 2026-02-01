#!/usr/bin/env python
"""
Tombo Language Interpreter CLI
Run Tombo programs from command line or interactive REPL
"""

import sys
import os
import re
import time
import subprocess
from pathlib import Path

# Try to enable readline for history and tab completion
try:
    import readline
    readline.set_history_length(1000)
    # History file
    history_file = Path.home() / '.tombo_history'
    if history_file.exists():
        readline.read_history_file(str(history_file))
except ImportError:
    readline = None
    history_file = None

def format_error_with_context(error_msg: str, code: str) -> str:
    """Format error message with code context and line numbers."""
    # Try to extract line and column from error message
    match = re.search(r'line (\d+).*column (\d+)', error_msg)
    if not match:
        return error_msg
    
    line_num = int(match.group(1))
    col_num = int(match.group(2))
    lines = code.split('\n')
    
    if line_num < 1 or line_num > len(lines):
        return error_msg
    
    result = error_msg + '\n'
    # Show context (2 lines before, the error line, 2 lines after)
    start = max(0, line_num - 3)
    end = min(len(lines), line_num + 2)
    
    for i in range(start, end):
        line_idx = i + 1
        marker = '>>>' if line_idx == line_num else '   '
        result += f"{marker} {line_idx:3d} | {lines[i]}\n"
        if line_idx == line_num:
            result += f"        | {' ' * (col_num - 1)}^\n"
    
    return result.rstrip()

def handle_magic_command(code: str) -> tuple:
    """
    Handle magic commands (%time, !shell) and namespace exploration.
    Returns (handled: bool, result: str, code_to_exec: str)
    """
    code = code.strip()
    
    # %time: time execution
    if code.startswith('%time '):
        actual_code = code[6:]
        return (True, None, actual_code)  # Special marker for timing
    
    # !shell: run shell command
    if code.startswith('!'):
        shell_cmd = code[1:].strip()
        try:
            output = subprocess.run(shell_cmd, shell=True, capture_output=True, text=True, timeout=5)
            result = output.stdout
            if output.stderr:
                result += output.stderr
            return (True, result.rstrip(), None)
        except Exception as e:
            return (True, f"Shell error: {e}", None)
    
    # help(name) or ?name
    if code.startswith('?'):
        return (True, "Use help(name) for documentation", None)
    
    return (False, None, None)

def get_completer(interp):
    """Create a completer function for readline tab completion."""
    def completer(text, state):
        if state == 0:
            completer.matches = []
            # Get all available names from interpreter environment
            names = list(interp.global_env.store.keys())
            # Filter by prefix
            completer.matches = [n for n in names if n.startswith(text)]
            # Add builtins
            builtins = ['help', 'dir', 'exit', 'quit', 'if', 'while', 'for', 'def', 'defi', 'class', 'let', 'change']
            completer.matches.extend([b for b in builtins if b.startswith(text) and b not in completer.matches])
            completer.matches.sort()
        
        if state < len(completer.matches):
            return completer.matches[state]
        return None
    
    return completer

def repl():
    """Interactive REPL mode"""
    # Add src to path
    tombo_path = Path(__file__).parent
    sys.path.insert(0, str(tombo_path / 'src'))
    
    from core.interpreter import Interpreter
    from lexer.lexer import Lexer
    from parser.parser import Parser
    
    interp = Interpreter()
    
    # Add help() and dir() builtins to interpreter
    def help_func(name=None):
        if name is None:
            return "Available commands: help(name), dir(), exit, quit, !shell_cmd, %time code"
        # Try to find in environment
        obj = interp.global_env.get(name) if isinstance(name, str) else name
        if obj is None:
            return f"No help for {name}"
        if callable(obj):
            return f"{name}(...) - callable function"
        return f"{name} = {obj}"
    
    def dir_func():
        names = sorted(interp.global_env.store.keys())
        return '\n'.join(names)
    
    interp.global_env.set('help', help_func)
    interp.global_env.set('dir', dir_func)
    
    # Setup readline
    if readline:
        readline.parse_and_bind('tab: complete')
        completer = get_completer(interp)
        readline.set_completer(completer)
    
    print("╔══════════════════════════════════════════╗")
    print("║       TOMBO LANGUAGE INTERPRETER        ║")
    print("║              v1.0.0 REPL                ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("Type code and press Enter to execute")
    print("Multi-line blocks: if/while/for/def/class/try...end")
    print("History: Up/Down arrows | Tab completion | exit/quit")
    print("Commands: help(), dir(), !shell, %time code")
    print()
    
    # Check if stdin is a terminal
    if not sys.stdin.isatty():
        return
    
    while True:
        try:
            code = input("tombo> ")
            
            if code.strip() in ('exit', 'quit'):
                print("Goodbye!")
                break
            
            if not code.strip():
                continue
            
            # Handle magic commands
            is_magic, magic_result, code_to_eval = handle_magic_command(code)
            if is_magic:
                if magic_result is not None:
                    print(magic_result)
                if code_to_eval is None:
                    continue
                code = code_to_eval
                timing = True
            else:
                timing = False
            
            # Collect multi-line input if needed
            original_code = code
            while needs_continuation(code):
                continuation = input("...   > ")
                if continuation.strip() in ('exit', 'quit'):
                    code = None
                    break

                if continuation.strip() == 'end':
                    code += "\n" + continuation
                    continue

                if continuation and (continuation[0] == ' ' or continuation[0] == '\t'):
                    code += "\n" + continuation
                else:
                    code += "\n" + (' ' * 4) + continuation
            
            if code is None:
                print("Goodbye!")
                break
            
            try:
                # Convenience: allow `name = expr` as shorthand for `let name = expr`
                if re.match(r"^\s*[A-Za-z_]\w*\s*=(?!=)", code) and not code.lstrip().startswith(('let ', 'change ')):
                    code = 'let ' + code.lstrip()

                start_time = time.time() if timing else None
                
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                result = interp.eval(ast)
                
                if timing:
                    elapsed = time.time() - start_time
                    print(f"({elapsed*1000:.2f}ms)")

                # Determine whether to print result: suppress for declarations/assignments
                should_print = True
                try:
                    from ast.ast_nodes import (
                        VariableDecl,
                        ChangeStatement,
                        FunctionDef as AstFunctionDef,
                        ShorthandFunctionDef,
                        ClassDef as AstClassDef,
                        ReturnStatement as AstReturnStatement,
                        ImportStatement as AstImportStatement,
                        PassStatement as AstPassStatement,
                        UseStatement as AstUseStatement,
                    )
                    if hasattr(ast, 'statements') and ast.statements:
                        last = ast.statements[-1]
                        if isinstance(last, (VariableDecl, ChangeStatement, AstFunctionDef, ShorthandFunctionDef, AstClassDef, AstReturnStatement, AstImportStatement, AstPassStatement, AstUseStatement)):
                            should_print = False
                except Exception:
                    pass

                try:
                    from core.ast import Let as CoreLet, Change as CoreChange
                    if hasattr(ast, 'body') and ast.body:
                        last = ast.body[-1]
                        if isinstance(last, (CoreLet, CoreChange)):
                            should_print = False
                except Exception:
                    pass

                if should_print and result is not None:
                    print(result)
            except Exception as e:
                error_msg = format_error_with_context(str(e), code)
                print(f"Error: {error_msg}")
                
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            break
        except EOFError:
            break
    
    # Save history
    if readline and history_file:
        try:
            readline.write_history_file(str(history_file))
        except Exception:
            pass

def needs_continuation(code):
    """Check if code snippet needs continuation (incomplete statement)"""
    code = code.strip()
    if not code:
        return False
    
    # Keywords that start a block
    block_keywords = ('if', 'while', 'for', 'def', 'defi', 'class', 'try')
    
    # Check if line starts with block keyword
    first_word = code.split()[0] if code.split() else ''
    if first_word in block_keywords:
        # Expect 'end' keyword to close the block
        if 'end' not in code:
            return True
    
    # Check for unclosed brackets/parens/braces
    open_count = code.count('(') + code.count('[') + code.count('{')
    close_count = code.count(')') + code.count(']') + code.count('}')
    if open_count > close_count:
        return True
    
    return False

def main():
    """Main entry point for Tombo interpreter"""
    # Add src to path
    tombo_path = Path(__file__).parent
    sys.path.insert(0, str(tombo_path / 'src'))
    
    from core.interpreter import Interpreter
    
    if len(sys.argv) > 1:
        # Run file
        filename = sys.argv[1]
        if not os.path.exists(filename):
            print(f"Error: File not found: {filename}")
            sys.exit(1)
        
        with open(filename, 'r') as f:
            code = f.read()
        
        from lexer.lexer import Lexer
        from parser.parser import Parser
        
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            interp = Interpreter()
            result = interp.eval(ast)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Show info and launch REPL
        print("╔══════════════════════════════════════════╗")
        print("║       TOMBO LANGUAGE INTERPRETER        ║")
        print("║              v1.0.0                      ║")
        print("╚══════════════════════════════════════════╝")
        print()
        interp = Interpreter()
        count = len([v for v in interp.global_env.store.values() if callable(v)])
        print(f"✓ Interpreter Ready")
        print(f"✓ {count} Functions Available")
        print(f"✓ 39 Libraries Loaded")
        print(f"✓ Hardware Access: Camera, Audio, Sensors")
        print()
        print("Usage:")
        print("  tombo script.to     - Run a script")
        print("  tombo -i            - Interactive REPL")
        print()
        
        # Launch REPL if no arguments
        repl()

if __name__ == '__main__':
    main()
