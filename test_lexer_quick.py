#!/usr/bin/env python
"""Quick test of the Tombo lexer."""
import sys
sys.path.insert(0, ".")

from src.lexer import Lexer, TokenType

def test_basic():
    """Test basic lexing."""
    print("=" * 60)
    print("TEST 1: Empty input")
    lexer = Lexer("")
    tokens = lexer.tokenize()
    assert tokens[-1].type == TokenType.EOF
    print("✓ PASS: Empty input tokenizes correctly")

    print("\nTEST 2: Simple number")
    lexer = Lexer("42")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == "42"
    print("✓ PASS: Number tokenization works")

    print("\nTEST 3: String literals")
    lexer = Lexer('"hello world"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "hello world"
    print("✓ PASS: String tokenization works")

    print("\nTEST 4: Keywords")
    lexer = Lexer("let change to def defi if else")
    tokens = lexer.tokenize()
    keyword_tokens = [t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
    assert tokens[0].type == TokenType.LET
    assert tokens[1].type == TokenType.CHANGE
    assert tokens[2].type == TokenType.TO
    print("✓ PASS: Keyword recognition works")

    print("\nTEST 5: Operators")
    lexer = Lexer("+ - * / = == !=")
    tokens = lexer.tokenize()
    ops = [t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
    print(f"  Operators found: {[(i, t.type.name) for i, t in enumerate(ops)]}")
    assert ops[0].type == TokenType.PLUS, f"Expected PLUS at 0, got {ops[0].type}"
    assert ops[1].type == TokenType.MINUS, f"Expected MINUS at 1, got {ops[1].type}"
    assert ops[5].type == TokenType.EQEQ, f"Expected EQEQ at 5, got {ops[5].type}"
    assert ops[6].type == TokenType.NEQ, f"Expected NEQ at 6, got {ops[6].type}"
    print("✓ PASS: Operator tokenization works")

def test_indentation():
    """Test indentation handling."""
    print("\n" + "=" * 60)
    print("TEST 6: Simple indentation")
    code = """if true
    println("yes")
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    indent_tokens = [t for t in tokens if t.type == TokenType.INDENT]
    dedent_tokens = [t for t in tokens if t.type == TokenType.DEDENT]
    
    assert len(indent_tokens) >= 1, f"Expected indents, got {indent_tokens}"
    assert len(dedent_tokens) >= 1, f"Expected dedents, got {dedent_tokens}"
    print("✓ PASS: Simple indentation works")

    print("\nTEST 7: Multiple indentation levels")
    code = """if true
    if true
        println("nested")
println("done")
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    indent_count = sum(1 for t in tokens if t.type == TokenType.INDENT)
    dedent_count = sum(1 for t in tokens if t.type == TokenType.DEDENT)
    
    assert indent_count >= 2, f"Expected 2+ indents, got {indent_count}"
    assert dedent_count >= 2, f"Expected 2+ dedents, got {dedent_count}"
    print("✓ PASS: Multiple indentation levels work")

def test_real_code():
    """Test real Tombo code snippets."""
    print("\n" + "=" * 60)
    print("TEST 8: CHANGE TO statement")
    code = "change x to 5"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    token_types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
    assert TokenType.CHANGE in token_types
    assert TokenType.TO in token_types
    print("✓ PASS: CHANGE TO syntax works")

    print("\nTEST 9: DEFI shorthand function")
    code = "defi double(x) => x * 2"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    token_types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
    assert TokenType.DEFI in token_types
    assert TokenType.ARROW in token_types
    print("✓ PASS: DEFI syntax works")

    print("\nTEST 10: Function with block")
    code = """def greet(name)
    println("Hello")
end
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    token_types = [t.type for t in tokens]
    assert TokenType.DEF in token_types
    assert TokenType.END in token_types
    assert TokenType.INDENT in token_types
    print("✓ PASS: DEF with block syntax works")

if __name__ == "__main__":
    try:
        test_basic()
        test_indentation()
        test_real_code()
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
