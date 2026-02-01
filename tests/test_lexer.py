"""
Comprehensive tests for the Tombo lexer.
Tests indentation handling, tokens, and edge cases.
"""
import pytest
from src.lexer import Lexer, TokenType, Token


class TestLexerBasics:
    """Test basic lexer functionality."""

    def test_empty_input(self):
        """Test lexing empty input."""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        assert tokens[-1].type == TokenType.EOF

    def test_single_number(self):
        """Test lexing a single number."""
        lexer = Lexer("42")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == "42"

    def test_float_number(self):
        """Test lexing float literals."""
        lexer = Lexer("3.14")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == "3.14"

    def test_scientific_notation(self):
        """Test lexing scientific notation."""
        lexer = Lexer("1.5e-10")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == "1.5e-10"

    def test_string_literals(self):
        """Test lexing string literals."""
        lexer = Lexer('"hello"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello"

        lexer = Lexer("'world'")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "world"

    def test_string_escape_sequences(self):
        """Test string escape sequences."""
        lexer = Lexer(r'"hello\nworld"')
        tokens = lexer.tokenize()
        assert tokens[0].value == "hello\nworld"

    def test_identifiers(self):
        """Test lexing identifiers."""
        lexer = Lexer("my_variable x foo123 _private")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "my_variable"
        assert tokens[2].type == TokenType.IDENTIFIER
        assert tokens[4].type == TokenType.IDENTIFIER
        assert tokens[6].type == TokenType.IDENTIFIER


class TestLexerKeywords:
    """Test keyword recognition."""

    def test_keywords(self):
        """Test that keywords are recognized."""
        keywords = [
            "let",
            "change",
            "to",
            "def",
            "defi",
            "if",
            "else",
            "elif",
            "for",
            "while",
            "in",
            "end",
            "return",
            "match",
            "when",
            "class",
            "self",
            "import",
            "try",
            "catch",
            "finally",
            "async",
            "await",
        ]

        for keyword in keywords:
            lexer = Lexer(keyword)
            tokens = lexer.tokenize()
            assert tokens[0].type.name == keyword.upper()

    def test_boolean_literals(self):
        """Test boolean literals."""
        lexer = Lexer("true false")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.BOOLEAN
        assert tokens[0].value == "true"
        assert tokens[2].type == TokenType.BOOLEAN
        assert tokens[2].value == "false"


class TestLexerOperators:
    """Test operator tokenization."""

    def test_single_char_operators(self):
        """Test single character operators."""
        lexer = Lexer("+ - * / % . , : = < > & | ^ ~")
        tokens = lexer.tokenize()
        operators = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.PERCENT,
            TokenType.DOT,
            TokenType.COMMA,
            TokenType.COLON,
            TokenType.EQ,
            TokenType.LT,
            TokenType.GT,
            TokenType.AMPERSAND,
            TokenType.PIPE,
            TokenType.CARET,
            TokenType.TILDE,
        ]
        token_list = [
            t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)
        ]
        for token, expected in zip(token_list, operators):
            assert token.type == expected

    def test_double_char_operators(self):
        """Test double character operators."""
        lexer = Lexer("=> == != <= >= << >> += -= *= /=")
        tokens = lexer.tokenize()
        operators = [
            TokenType.ARROW,
            TokenType.EQEQ,
            TokenType.NEQ,
            TokenType.LTE,
            TokenType.GTE,
            TokenType.LSHIFT,
            TokenType.RSHIFT,
            TokenType.PLUSEQ,
            TokenType.MINUSEQ,
            TokenType.STAREQ,
            TokenType.SLASHEQ,
        ]
        token_list = [
            t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)
        ]
        for token, expected in zip(token_list, operators):
            assert token.type == expected

    def test_power_operator(self):
        """Test power operator."""
        lexer = Lexer("**")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.POWER


class TestLexerDelimiters:
    """Test delimiter tokenization."""

    def test_parentheses(self):
        """Test parentheses."""
        lexer = Lexer("( )")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[2].type == TokenType.RPAREN

    def test_brackets(self):
        """Test brackets."""
        lexer = Lexer("[ ]")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LBRACKET
        assert tokens[2].type == TokenType.RBRACKET

    def test_braces(self):
        """Test braces."""
        lexer = Lexer("{ }")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LBRACE
        assert tokens[2].type == TokenType.RBRACE


class TestLexerIndentation:
    """Test indentation handling - CRITICAL for Tombo."""

    def test_simple_indent(self):
        """Test simple indentation."""
        code = """if true
    println("yes")
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Find INDENT token
        indent_tokens = [t for t in tokens if t.type == TokenType.INDENT]
        assert len(indent_tokens) >= 1

    def test_indent_dedent(self):
        """Test indent and dedent."""
        code = """if true
    println("yes")
println("done")
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        indent_count = sum(1 for t in tokens if t.type == TokenType.INDENT)
        dedent_count = sum(1 for t in tokens if t.type == TokenType.DEDENT)

        # Should have at least one indent and one dedent
        assert indent_count >= 1
        assert dedent_count >= 1

    def test_multiple_indent_levels(self):
        """Test multiple indentation levels."""
        code = """if true
    if true
        println("nested")
println("done")
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        indent_count = sum(1 for t in tokens if t.type == TokenType.INDENT)
        dedent_count = sum(1 for t in tokens if t.type == TokenType.DEDENT)

        # Should have 2 indents and 2 dedents
        assert indent_count >= 2
        assert dedent_count >= 2

    def test_dedent_multiple_levels(self):
        """Test dedenting multiple levels at once."""
        code = """if true
    if true
        println("nested")
println("done")
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Find positions of dedents
        dedent_indices = [i for i, t in enumerate(tokens) if t.type == TokenType.DEDENT]
        assert len(dedent_indices) >= 2

    def test_skip_blank_lines(self):
        """Test that blank lines are skipped."""
        code = """let x = 1

let y = 2
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Should have tokens for both let statements
        let_tokens = [t for t in tokens if t.type == TokenType.LET]
        assert len(let_tokens) == 2

    def test_skip_comment_lines(self):
        """Test that comment-only lines are skipped."""
        code = """let x = 1
# This is a comment
let y = 2
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        let_tokens = [t for t in tokens if t.type == TokenType.LET]
        assert len(let_tokens) == 2

    def test_comments_removed(self):
        """Test that comments are removed."""
        code = "let x = 1 # assign x"
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT]
        assert len(comment_tokens) == 0


class TestLexerLineTracking:
    """Test line and column tracking for error reporting."""

    def test_line_numbers(self):
        """Test that line numbers are tracked correctly."""
        code = """let x = 1
let y = 2
let z = 3
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        let_tokens = [t for t in tokens if t.type == TokenType.LET]
        assert let_tokens[0].line == 1
        assert let_tokens[1].line == 2
        assert let_tokens[2].line == 3

    def test_column_numbers(self):
        """Test that column numbers are tracked correctly."""
        code = "let x = 1"
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        assert tokens[0].column == 1  # 'let' starts at column 1
        assert tokens[2].column == 5  # 'x' starts at column 5


class TestLexerComplexCode:
    """Test lexer on real code examples."""

    def test_change_statement(self):
        """Test CHANGE TO syntax."""
        code = """change x to 5
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        token_types = [t.type for t in tokens if t.type != TokenType.NEWLINE]
        assert TokenType.CHANGE in token_types
        assert TokenType.TO in token_types

    def test_defi_function(self):
        """Test DEFI shorthand function."""
        code = """defi double(x) => x * 2
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        token_types = [t.type for t in tokens if t.type != TokenType.NEWLINE]
        assert TokenType.DEFI in token_types
        assert TokenType.ARROW in token_types

    def test_if_block(self):
        """Test IF statement with block."""
        code = """if x > 10
    println("big")
else
    println("small")
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        token_types = [t.type for t in tokens]
        assert TokenType.IF in token_types
        assert TokenType.ELSE in token_types
        assert TokenType.INDENT in token_types
        assert TokenType.DEDENT in token_types

    def test_function_definition(self):
        """Test function definition."""
        code = """def greet(name)
    println("Hello, " + name)
end
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        token_types = [t.type for t in tokens]
        assert TokenType.DEF in token_types
        assert TokenType.END in token_types

    def test_class_definition(self):
        """Test class definition."""
        code = """class Person
    def init(name)
        self.name = name
    end
end
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        token_types = [t.type for t in tokens]
        assert TokenType.CLASS in token_types
        assert TokenType.SELF in token_types

    def test_match_statement(self):
        """Test MATCH statement."""
        code = """match x
    when 1: "one"
    when 2: "two"
    else: "other"
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        token_types = [t.type for t in tokens]
        assert TokenType.MATCH in token_types
        assert TokenType.WHEN in token_types

    def test_try_catch(self):
        """Test TRY-CATCH."""
        code = """try
    risky_operation()
catch error
    println(error)
finally
    cleanup()
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        token_types = [t.type for t in tokens]
        assert TokenType.TRY in token_types
        assert TokenType.CATCH in token_types
        assert TokenType.FINALLY in token_types


class TestLexerErrors:
    """Test error handling."""

    def test_unterminated_string(self):
        """Test error on unterminated string."""
        lexer = Lexer('"hello')
        with pytest.raises(Exception):  # Should raise LexerError
            lexer.tokenize()

    def test_unexpected_character(self):
        """Test error on unexpected character."""
        lexer = Lexer("@invalid")
        with pytest.raises(Exception):  # Should raise LexerError
            lexer.tokenize()

    def test_indentation_error(self):
        """Test error on inconsistent indentation."""
        code = """if true
  println("bad")
    println("inconsistent")
"""
        lexer = Lexer(code)
        with pytest.raises(Exception):  # Should raise LexerError
            lexer.tokenize()


class TestLexerEdgeCases:
    """Test edge cases."""

    def test_mixed_operators(self):
        """Test mixing different operators."""
        code = "x = y + z * 2 / 3 - 1"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert len([t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]) > 0

    def test_chained_method_calls(self):
        """Test chained method calls."""
        code = "x.foo().bar().baz()"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        dot_count = sum(1 for t in tokens if t.type == TokenType.DOT)
        assert dot_count >= 2

    def test_list_literal(self):
        """Test list literal."""
        code = "[1, 2, 3, 4, 5]"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LBRACKET
        assert tokens[-2].type == TokenType.RBRACKET

    def test_dict_literal(self):
        """Test dictionary literal."""
        code = '{"key": "value", "x": 42}'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LBRACE
        colon_count = sum(1 for t in tokens if t.type == TokenType.COLON)
        assert colon_count >= 2

    def test_negative_number(self):
        """Test negative numbers."""
        code = "-42"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # This will be tokenized as MINUS followed by NUMBER
        # The parser will handle making it negative
        assert tokens[0].type == TokenType.MINUS


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
