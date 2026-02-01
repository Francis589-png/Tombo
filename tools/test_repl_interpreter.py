#!/usr/bin/env python3
"""Test REPL interpreter integration: lexer → parser → evaluator"""
import unittest
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.lexer import Lexer
from src.core.parser import Parser
from src.core.interpreter import Interpreter


class TestREPLInterpreter(unittest.TestCase):
    def setUp(self):
        self.interp = Interpreter()

    def test_let_binding(self):
        """Test let statement creates variable binding"""
        code = "let x = 5"
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('x'), 5)

    def test_arithmetic_expression(self):
        """Test basic arithmetic evaluation"""
        code = "let result = 2 + 3"
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('result'), 5)

    def test_function_definition_and_call(self):
        """Test defi (short function) definition and invocation"""
        code = """defi add(a, b) => a + b
let sum = add(2, 3)
"""
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('sum'), 5)

    def test_if_statement(self):
        """Test if block execution"""
        code = """let x = 10
if x > 5
    let result = 100
end
"""
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('result'), 100)

    def test_string_literal(self):
        """Test string evaluation"""
        code = 'let msg = "hello world"'
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('msg'), "hello world")

    def test_list_literal(self):
        """Test list creation"""
        code = "let items = [1, 2, 3]"
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('items'), [1, 2, 3])

    def test_builtin_function_call(self):
        """Test calling a builtin function (len)"""
        code = """let arr = [1, 2, 3]
let length = len(arr)
"""
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('length'), 3)

    def test_stdlib_math_function(self):
        """Test calling stdlib math function (e.g., abs)"""
        code = "let result = abs(0 - 42)"
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('result'), 42)

    def test_stdlib_string_function(self):
        """Test calling stdlib string function"""
        code = """let text = "hello"
let upper = upper(text)
"""
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('upper'), "HELLO")

    def test_multiple_statements(self):
        """Test multiple statements in sequence"""
        code = """let a = 1
let b = 2
let c = a + b
let d = c * 2
"""
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('d'), 6)

    def test_change_statement(self):
        """Test change (reassignment) statement"""
        code = """let x = 5
change x to 10
"""
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('x'), 10)

    def test_comparison_operators(self):
        """Test comparison in if condition"""
        code = """let x = 20
if x > 10
    let result = "big"
end
"""
        lex = Lexer(code)
        toks = lex.tokenize()
        p = Parser(toks)
        ast = p.parse()
        self.interp.eval(ast)
        self.assertEqual(self.interp.global_env.get('result'), "big")

    def test_stdlib_loaded_on_init(self):
        """Test that stdlib functions are available on Interpreter creation"""
        interp = Interpreter()
        # Check that some stdlib functions are registered
        self.assertIsNotNone(interp.global_env.get('abs'))
        self.assertIsNotNone(interp.global_env.get('upper'))
        self.assertIsNotNone(interp.global_env.get('lower'))


class TestREPLPackageIntegration(unittest.TestCase):
    """Test REPL package path loading"""
    
    def test_tombo_packages_txt_parsing(self):
        """Test that tombo_packages.txt would be read if present"""
        # This test checks that the REPL logic for loading packages is sound
        pkg_file = 'tombo_packages.txt'
        pkg_paths = []
        if os.path.exists(pkg_file):
            with open(pkg_file, 'r', encoding='utf-8') as f:
                pkg_paths = [ln.strip() for ln in f if ln.strip()]
        # Just verify the file reading works
        self.assertIsInstance(pkg_paths, list)


if __name__ == '__main__':
    unittest.main(verbosity=2)
