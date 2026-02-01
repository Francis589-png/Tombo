"""
Token type definitions for the Tombo lexer.
"""
from enum import Enum, auto


class LexerError(Exception):
    """Raised when lexer encounters an error."""

    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"{message} at line {line}, column {column}")


class TokenType(Enum):
    """All token types used by the Tombo lexer."""

    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    BOOLEAN = auto()

    # Keywords
    LET = auto()
    CHANGE = auto()
    TO = auto()
    DEF = auto()
    DEFI = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    FOR = auto()
    WHILE = auto()
    IN = auto()
    END = auto()
    RETURN = auto()
    MATCH = auto()
    WHEN = auto()
    CLASS = auto()
    SELF = auto()
    IMPORT = auto()
    USE = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    ASYNC = auto()
    AWAIT = auto()
    BREAK = auto()
    CONTINUE = auto()
    PASS = auto()
    THEN = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    POWER = auto()
    DOT = auto()
    COMMA = auto()
    COLON = auto()
    ARROW = auto()  # =>
    EQ = auto()  # =
    EQEQ = auto()  # ==
    NEQ = auto()  # !=
    LT = auto()  # <
    GT = auto()  # >
    LTE = auto()  # <=
    GTE = auto()  # >=
    AND = auto()  # and
    OR = auto()  # or
    NOT = auto()  # not
    AMPERSAND = auto()  # &
    PIPE = auto()  # |
    CARET = auto()  # ^
    TILDE = auto()  # ~
    LSHIFT = auto()  # <<
    RSHIFT = auto()  # >>
    PLUSEQ = auto()  # +=
    MINUSEQ = auto()  # -=
    STAREQ = auto()  # *=
    SLASHEQ = auto()  # /=

    # Delimiters
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    LBRACE = auto()  # {
    RBRACE = auto()  # }

    # Special
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    EOF = auto()

    # Comments (not normally tokens, but tracked)
    COMMENT = auto()


class Token:
    """Represents a single token in the source code."""

    def __init__(
        self, type_: TokenType, value: str, line: int, column: int, raw: str = None
    ):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
        self.raw = raw or value  # Original text from source

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (
            self.type == other.type
            and self.value == other.value
            and self.line == other.line
            and self.column == other.column
        )
