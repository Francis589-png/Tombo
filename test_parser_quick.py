#!/usr/bin/env python
"""Quick test of the Tombo parser."""
import sys
sys.path.insert(0, ".")

from src.lexer import Lexer
from src.parser import Parser
from src.ast import *

def test_parser():
    """Test parser functionality."""
    print("=" * 60)
    print("PARSER TESTS")
    print("=" * 60)

    # Test 1: Simple variable declaration
    print("\nTest 1: Variable declaration (let x = 5)")
    code = "let x = 5"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], VariableDecl)
    assert ast.statements[0].name == "x"
    print("✓ PASS")

    # Test 2: Change statement
    print("\nTest 2: Change statement (change x to 10)")
    code = "change x to 10"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], ChangeStatement)
    print("✓ PASS")

    # Test 3: Simple function (defi)
    print("\nTest 3: Shorthand function (defi double(x) => x * 2)")
    code = "defi double(x) => x * 2"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], ShorthandFunctionDef)
    assert ast.statements[0].name == "double"
    assert len(ast.statements[0].params) == 1
    print("✓ PASS")

    # Test 4: Binary operation
    print("\nTest 4: Binary operation (2 + 3 * 4)")
    code = "2 + 3 * 4"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    expr = ast.statements[0]
    assert isinstance(expr, BinaryOp)
    assert expr.operator == "+"
    # Right side should be multiplication (higher precedence)
    assert isinstance(expr.right, BinaryOp)
    assert expr.right.operator == "*"
    print("✓ PASS")

    # Test 5: List literal
    print("\nTest 5: List literal ([1, 2, 3])")
    code = "[1, 2, 3]"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], ListLiteral)
    assert len(ast.statements[0].elements) == 3
    print("✓ PASS")

    # Test 6: Function call
    print("\nTest 6: Function call (println(42))")
    code = "println(42)"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], FunctionCall)
    assert len(ast.statements[0].args) == 1
    print("✓ PASS")

    # Test 7: Member access
    print("\nTest 7: Member access (obj.property)")
    code = "obj.property"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], MemberAccess)
    assert ast.statements[0].property == "property"
    print("✓ PASS")

    # Test 8: Index access
    print("\nTest 8: Index access (arr[0])")
    code = "arr[0]"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], IndexExpr)
    print("✓ PASS")

    # Test 9: If statement
    print("\nTest 9: If statement")
    code = """if x > 5
    println("big")
else
    println("small")
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], IfStatement)
    assert len(ast.statements[0].then_block) > 0
    assert len(ast.statements[0].else_block) > 0
    print("✓ PASS")

    # Test 10: For loop
    print("\nTest 10: For loop")
    code = """for x in [1, 2, 3]
    println(x)
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast.statements[0], ForLoop)
    assert ast.statements[0].variable == "x"
    print("✓ PASS")

    print("\n" + "=" * 60)
    print("ALL PARSER TESTS PASSED! ✓")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_parser()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
