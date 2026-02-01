#!/usr/bin/env python3
"""Performance profiling for Tombo interpreter and standard library."""
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.core.interpreter import Interpreter
from src.core.lexer import Lexer
from src.core.parser import Parser


def profile_interpreter_startup():
    """Measure interpreter initialization time."""
    start = time.perf_counter()
    interp = Interpreter()
    end = time.perf_counter()
    return end - start


def profile_stdlib_function_calls():
    """Measure execution time for stdlib function calls."""
    interp = Interpreter()
    
    # Math function
    code_math = "let result = abs(42)"
    lex = Lexer(code_math)
    toks = lex.tokenize()
    p = Parser(toks)
    ast = p.parse()
    
    start = time.perf_counter()
    for _ in range(1000):
        interp.eval(ast)
    end = time.perf_counter()
    math_time = end - start
    
    # String function
    code_str = 'let result = upper("test")'
    lex = Lexer(code_str)
    toks = lex.tokenize()
    p = Parser(toks)
    ast = p.parse()
    
    start = time.perf_counter()
    for _ in range(1000):
        interp.eval(ast)
    end = time.perf_counter()
    str_time = end - start
    
    return {'math': math_time, 'string': str_time}


def profile_lexer_parser():
    """Measure lexer + parser performance."""
    code = """let x = 5
if x > 0
    defi add(a, b) => a + b
    let result = add(2, 3)
end
"""
    
    start = time.perf_counter()
    for _ in range(100):
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
    end = time.perf_counter()
    
    return end - start


def profile_full_execution():
    """Measure full pipeline: lex + parse + eval."""
    code = """let x = 10
let y = 20
let z = x + y
"""
    
    start = time.perf_counter()
    for _ in range(100):
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        interp = Interpreter()
        interp.eval(ast)
    end = time.perf_counter()
    
    return end - start


def main():
    print("=" * 70)
    print("TOMBO PERFORMANCE PROFILING")
    print("=" * 70)
    print()
    
    # Interpreter startup
    print("INTERPRETER STARTUP")
    print("-" * 70)
    startup_time = profile_interpreter_startup()
    print(f"Interpreter init:        {startup_time*1000:.2f}ms")
    print()
    
    # Stdlib function calls
    print("STDLIB FUNCTION CALLS (1000 iterations)")
    print("-" * 70)
    func_times = profile_stdlib_function_calls()
    print(f"Math function (abs):     {func_times['math']*1000:.2f}ms")
    print(f"String function (upper): {func_times['string']*1000:.2f}ms")
    print(f"Avg per call:            {(func_times['math']/1000)*1e6:.2f}µs (math)")
    print()
    
    # Lexer + Parser
    print("LEXER + PARSER (100 iterations)")
    print("-" * 70)
    lex_parse_time = profile_lexer_parser()
    print(f"Lex + parse:             {lex_parse_time*1000:.2f}ms")
    print(f"Avg per iteration:       {(lex_parse_time/100)*1e6:.2f}µs")
    print()
    
    # Full pipeline
    print("FULL PIPELINE (100 iterations)")
    print("-" * 70)
    full_time = profile_full_execution()
    print(f"Full execution:          {full_time*1000:.2f}ms")
    print(f"Avg per iteration:       {(full_time/100)*1e6:.2f}µs")
    print()
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Interpreter ready in:    {startup_time*1000:.2f}ms")
    print(f"Function call latency:   {(func_times['math']/1000)*1e6:.2f}µs")
    print(f"Parse latency:           {(lex_parse_time/100)*1e6:.2f}µs")
    print(f"Typical REPL latency:    {(full_time/100)*1e6:.2f}µs")
    print()


if __name__ == '__main__':
    main()
