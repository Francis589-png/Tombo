"""
Lexer (tokenizer) for the Tombo language.
Handles indentation-based syntax with INDENT/DEDENT tokens.
"""
from typing import List, Optional
from .token_types import Token, TokenType, LexerError


class Lexer:
    """Tokenizes Tombo source code with indentation-aware tokens."""

    KEYWORDS = {
        "let": TokenType.LET,
        "change": TokenType.CHANGE,
        "to": TokenType.TO,
        "def": TokenType.DEF,
        "defi": TokenType.DEFI,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "elif": TokenType.ELIF,
        "for": TokenType.FOR,
        "while": TokenType.WHILE,
        "in": TokenType.IN,
        "end": TokenType.END,
        "return": TokenType.RETURN,
        "match": TokenType.MATCH,
        "when": TokenType.WHEN,
        "class": TokenType.CLASS,
        "self": TokenType.SELF,
        "import": TokenType.IMPORT,
        "use": TokenType.USE,
        "try": TokenType.TRY,
        "catch": TokenType.CATCH,
        "finally": TokenType.FINALLY,
        "async": TokenType.ASYNC,
        "await": TokenType.AWAIT,
        "break": TokenType.BREAK,
        "continue": TokenType.CONTINUE,
        "pass": TokenType.PASS,
        "then": TokenType.THEN,
        "true": TokenType.BOOLEAN,
        "false": TokenType.BOOLEAN,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.indent_stack = [0]  # Track indentation levels
        self.at_line_start = True
        self.pending_dedents = 0
        self.paren_depth = 0  # Track parentheses/brackets/braces

    def error(self, message: str) -> None:
        """Raise a lexer error."""
        raise LexerError(message, self.line, self.column)

    def peek(self, offset: int = 0) -> Optional[str]:
        """Look ahead at character without consuming."""
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None

    def advance(self) -> Optional[str]:
        """Consume and return the current character."""
        if self.pos >= len(self.source):
            return None

        char = self.source[self.pos]
        self.pos += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def skip_whitespace(self) -> None:
        """Skip spaces and tabs (but not newlines)."""
        while self.peek() in (" ", "\t"):
            self.advance()

    def skip_comment(self) -> None:
        """Skip comments starting with #."""
        if self.peek() == "#":
            while self.peek() and self.peek() != "\n":
                self.advance()

    def read_string(self, quote: str) -> str:
        """Read a string literal."""
        value = ""
        self.advance()  # Skip opening quote

        while True:
            char = self.peek()
            if char is None:
                self.error(f"Unterminated string literal")
            elif char == quote:
                self.advance()  # Skip closing quote
                break
            elif char == "\\":
                self.advance()
                next_char = self.advance()
                if next_char is None:
                    self.error("Unterminated string escape")
                # Handle escape sequences
                escape_map = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    "\\": "\\",
                    '"': '"',
                    "'": "'",
                    "0": "\0",
                }
                value += escape_map.get(next_char, next_char)
            else:
                value += self.advance()

        return value

    def read_number(self) -> str:
        """Read a numeric literal (int or float)."""
        value = ""

        # Handle negative numbers
        if self.peek() == "-":
            value += self.advance()

        # Read digits
        while self.peek() and self.peek().isdigit():
            value += self.advance()

        # Handle floats
        if self.peek() == "." and self.peek(1) and self.peek(1).isdigit():
            value += self.advance()  # Add '.'
            while self.peek() and self.peek().isdigit():
                value += self.advance()

        # Handle scientific notation
        if self.peek() and self.peek() in ("e", "E"):
            value += self.advance()
            if self.peek() in ("+", "-"):
                value += self.advance()
            while self.peek() and self.peek().isdigit():
                value += self.advance()

        return value

    def read_identifier(self) -> str:
        """Read an identifier or keyword."""
        value = ""
        while self.peek() and (self.peek().isalnum() or self.peek() in ("_", "?")):
            value += self.advance()
        return value

    def handle_line_start_indent(self) -> None:
        """Handle indentation at the start of a line."""
        if not self.at_line_start:
            return

        self.at_line_start = False

        # Skip blank lines and comment-only lines
        indent = 0
        temp_pos = self.pos

        while self.peek() in (" ", "\t"):
            if self.peek() == " ":
                indent += 1
            else:  # tab
                indent += 8  # Treat tab as 8 spaces
            self.advance()

        # Check if line is blank or comment-only
        if self.peek() in (None, "\n", "#"):
            # Skip this line
            while self.peek() and self.peek() != "\n":
                self.advance()
            if self.peek() == "\n":
                self.advance()
            self.at_line_start = True
            return

        # Reset position
        self.pos = temp_pos
        self.column = 1

        # Now actually handle indentation
        indent = 0
        while self.peek() in (" ", "\t"):
            if self.peek() == " ":
                indent += 1
            else:  # tab
                indent += 8
            self.advance()

        current_indent = self.indent_stack[-1]

        if indent > current_indent:
            # Increased indentation
            self.indent_stack.append(indent)
            self.tokens.append(
                Token(TokenType.INDENT, "", self.line, self.column, "")
            )
        elif indent < current_indent:
            # Decreased indentation
            while self.indent_stack and self.indent_stack[-1] > indent:
                self.indent_stack.pop()
                self.tokens.append(
                    Token(TokenType.DEDENT, "", self.line, self.column, "")
                )

            if self.indent_stack[-1] != indent:
                self.error(f"Indentation error: inconsistent indentation")

    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        while self.pos < len(self.source):
            # Handle indentation at line start
            self.handle_line_start_indent()

            # Skip whitespace (spaces/tabs in the middle of lines)
            if self.peek() in (" ", "\t"):
                self.skip_whitespace()
                continue

            # Skip comments
            if self.peek() == "#":
                self.skip_comment()
                continue

            # Newline
            if self.peek() == "\n":
                if (
                    self.paren_depth == 0
                    and self.tokens
                    and self.tokens[-1].type != TokenType.NEWLINE
                ):
                    self.tokens.append(
                        Token(TokenType.NEWLINE, "\n", self.line, self.column)
                    )
                self.advance()
                self.at_line_start = True
                continue

            # String literals
            if self.peek() and self.peek() in ('"', "'"):
                quote = self.peek()
                start_line, start_col = self.line, self.column
                value = self.read_string(quote)
                self.tokens.append(
                    Token(TokenType.STRING, value, start_line, start_col)
                )
                continue

            # Numbers
            if self.peek() and self.peek().isdigit():
                start_line, start_col = self.line, self.column
                value = self.read_number()
                self.tokens.append(
                    Token(TokenType.NUMBER, value, start_line, start_col)
                )
                continue

            # Identifiers and keywords
            if self.peek() and (self.peek().isalpha() or self.peek() == "_"):
                start_line, start_col = self.line, self.column
                value = self.read_identifier()
                token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
                self.tokens.append(
                    Token(token_type, value, start_line, start_col)
                )
                continue

            # Operators and delimiters
            start_line, start_col = self.line, self.column
            char = self.peek()

            # Two-character operators (build safely in case peek() is None)
            p0 = self.peek() or ""
            p1 = self.peek(1) or ""
            two_char = p0 + p1
            token_type = None
            value = char

            if two_char == "=>":
                self.advance()
                self.advance()
                token_type = TokenType.ARROW
                value = "=>"
            elif two_char == "==":
                self.advance()
                self.advance()
                token_type = TokenType.EQEQ
                value = "=="
            elif two_char == "!=":
                self.advance()
                self.advance()
                token_type = TokenType.NEQ
                value = "!="
            elif two_char == "<=":
                self.advance()
                self.advance()
                token_type = TokenType.LTE
                value = "<="
            elif two_char == ">=":
                self.advance()
                self.advance()
                token_type = TokenType.GTE
                value = ">="
            elif two_char == "<<":
                self.advance()
                self.advance()
                token_type = TokenType.LSHIFT
                value = "<<"
            elif two_char == ">>":
                self.advance()
                self.advance()
                token_type = TokenType.RSHIFT
                value = ">>"
            elif two_char == "+=":
                self.advance()
                self.advance()
                token_type = TokenType.PLUSEQ
                value = "+="
            elif two_char == "-=":
                self.advance()
                self.advance()
                token_type = TokenType.MINUSEQ
                value = "-="
            elif two_char == "*=":
                self.advance()
                self.advance()
                token_type = TokenType.STAREQ
                value = "*="
            elif two_char == "/=":
                self.advance()
                self.advance()
                token_type = TokenType.SLASHEQ
                value = "/="
            elif two_char == "**":
                self.advance()
                self.advance()
                token_type = TokenType.POWER
                value = "**"
            # Single character operators
            elif char == "+":
                self.advance()
                token_type = TokenType.PLUS
            elif char == "-":
                self.advance()
                token_type = TokenType.MINUS
            elif char == "*":
                self.advance()
                token_type = TokenType.STAR
            elif char == "/":
                self.advance()
                token_type = TokenType.SLASH
            elif char == "%":
                self.advance()
                token_type = TokenType.PERCENT
            elif char == ".":
                self.advance()
                token_type = TokenType.DOT
            elif char == ",":
                self.advance()
                token_type = TokenType.COMMA
            elif char == ":":
                self.advance()
                token_type = TokenType.COLON
            elif char == "=":
                self.advance()
                token_type = TokenType.EQ
            elif char == "<":
                self.advance()
                token_type = TokenType.LT
            elif char == ">":
                self.advance()
                token_type = TokenType.GT
            elif char == "&":
                self.advance()
                token_type = TokenType.AMPERSAND
            elif char == "|":
                self.advance()
                token_type = TokenType.PIPE
            elif char == "^":
                self.advance()
                token_type = TokenType.CARET
            elif char == "~":
                self.advance()
                token_type = TokenType.TILDE
            elif char == "(":
                self.advance()
                self.paren_depth += 1
                token_type = TokenType.LPAREN
            elif char == ")":
                self.advance()
                self.paren_depth -= 1
                token_type = TokenType.RPAREN
            elif char == "[":
                self.advance()
                self.paren_depth += 1
                token_type = TokenType.LBRACKET
            elif char == "]":
                self.advance()
                self.paren_depth -= 1
                token_type = TokenType.RBRACKET
            elif char == "{":
                self.advance()
                self.paren_depth += 1
                token_type = TokenType.LBRACE
            elif char == "}":
                self.advance()
                self.paren_depth -= 1
                token_type = TokenType.RBRACE
            else:
                self.error(f"Unexpected character: {char}")

            if token_type:
                self.tokens.append(Token(token_type, value, start_line, start_col))

        # Handle remaining dedents at end of file
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(
                Token(TokenType.DEDENT, "", self.line, self.column, "")
            )

        # Add final newline and EOF
        if self.tokens and self.tokens[-1].type != TokenType.NEWLINE:
            self.tokens.append(
                Token(TokenType.NEWLINE, "\n", self.line, self.column)
            )

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column, ""))

        return self.tokens
