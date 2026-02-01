"""
Simple indentation-aware lexer for Tombo (core).
This lexer produces INDENT/DEDENT/NEWLINE/EOF tokens and basic lexical tokens.
This is a starting implementation; domains and full token sets will be expanded.
"""
from enum import Enum, auto
import re

class TokenType(Enum):
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    EOF = auto()
    IDENT = auto()
    NUMBER = auto()
    STRING = auto()
    OP = auto()
    KEYWORD = auto()
    COLON = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()

KEYWORDS = {
    "let", "change", "def", "defi", "if", "elif", "else",
    "for", "while", "in", "return", "use", "end", "model",
    "class", "match", "when", "try", "catch", "finally",
}

TokenSpec = [
    (TokenType.STRING, r"\"([^\"\\]|\\.)*\"|'([^'\\]|\\.)*'"),
    (TokenType.NUMBER, r"\d+(?:\.\d+)?"),
    (TokenType.IDENT, r"[A-Za-z_][A-Za-z0-9_]*"),
    (TokenType.OP, r"==|!=|<=|>=|\+\+|--|\+|\-|\*|/|%|<|>|=|\.|\[|\]|\->"),
    (TokenType.COLON, r":"),
    (TokenType.COMMA, r","),
    (TokenType.LPAREN, r"\("),
    (TokenType.RPAREN, r"\)"),
    (None, r"\s+"),  # skip whitespace (inside a line)
]

MASTER_REGEX = re.compile("|".join(f"(?P<T{i}>{pat})" for i,(_,pat) in enumerate(TokenSpec)))

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.col})"

class Lexer:
    def __init__(self, source: str):
        # Normalize line endings
        self.source = source.replace('\r\n', '\n').replace('\r', '\n')
        self.lines = self.source.split('\n')
        self.indent_stack = [0]
        self.tokens = []

    def tokenize(self):
        for lineno, raw_line in enumerate(self.lines, start=1):
            line = raw_line.rstrip('\n')
            # Remove comments
            stripped_for_comment = line.split('#', 1)[0]
            if stripped_for_comment.strip() == "":
                # Blank or comment-only line -> emit NEWLINE to keep line numbering but ignore indentation changes
                self.tokens.append(Token(TokenType.NEWLINE, "\n", lineno, 1))
                continue

            leading = len(stripped_for_comment) - len(stripped_for_comment.lstrip(' '))
            # Indentation handling
            if leading > self.indent_stack[-1]:
                self.indent_stack.append(leading)
                self.tokens.append(Token(TokenType.INDENT, leading, lineno, 1))
            else:
                while leading < self.indent_stack[-1]:
                    self.indent_stack.pop()
                    self.tokens.append(Token(TokenType.DEDENT, None, lineno, 1))

            # Tokenize the content of the line
            col = leading + 1
            content = stripped_for_comment.lstrip(' ')
            pos = 0
            while pos < len(content):
                m = MASTER_REGEX.match(content, pos)
                if not m:
                    # Unknown character -> create OP token for single char
                    ch = content[pos]
                    self.tokens.append(Token(TokenType.OP, ch, lineno, col))
                    pos += 1
                    col += 1
                    continue
                group_name = m.lastgroup
                idx = int(group_name[1:])
                tok_type, _ = TokenSpec[idx]
                text = m.group(group_name)
                if tok_type is not None:
                    if tok_type is TokenType.IDENT and text in KEYWORDS:
                        ttype = TokenType.KEYWORD
                    else:
                        ttype = tok_type
                    self.tokens.append(Token(ttype, text, lineno, col))
                # advance
                adv = len(text)
                pos += adv
                col += adv
            # End of line
            self.tokens.append(Token(TokenType.NEWLINE, "\n", lineno, len(raw_line)))
        # After all lines, unwind indentation
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, None, len(self.lines), 1))
        self.tokens.append(Token(TokenType.EOF, None, len(self.lines)+1, 1))
        return self.tokens

if __name__ == '__main__':
    sample = '''let x = 5
if x > 0
    change x to 10
    defi add(a, b) => a + b
end
'''
    lexer = Lexer(sample)
    toks = lexer.tokenize()
    for t in toks:
        print(t)