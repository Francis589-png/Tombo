"""
A minimal recursive-descent parser for Tombo (core).
Parses a small subset: `let`, `change`, expression statements, `if` with indented blocks, and `defi` shorthand.
Returns a simple AST (nested dicts/lists) suitable for feeding into an interpreter later.
"""
from typing import List, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.core.lexer import Lexer, TokenType
from src.core.ast import Module, Let, Change, If, Defi, Number, String, Ident, Binary, FunctionDef, Call, ListLiteral, Return
from src.core.ast import Use

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[Any]):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        t = self.peek()
        if t:
            self.pos += 1
        return t

    def expect(self, type_, value=None):
        t = self.peek()
        if not t or t.type != type_ or (value is not None and t.value != value):
            raise ParserError(f"Expected {type_} {value}, got {t}")
        return self.advance()

    def parse(self):
        stmts = []
        while True:
            t = self.peek()
            if not t or t.type == TokenType.EOF:
                break
            if t.type == TokenType.NEWLINE:
                self.advance(); continue
            stmts.append(self.parse_statement())
        return Module(stmts)

    def parse_statement(self):
        t = self.peek()
        if t.type == TokenType.KEYWORD:
            if t.value == 'let':
                return self.parse_let()
            if t.value == 'use':
                return self.parse_use()
            if t.value == 'change':
                return self.parse_change()
            if t.value == 'if':
                return self.parse_if()
            if t.value == 'defi':
                return self.parse_defi()
            if t.value == 'def':
                return self.parse_def()
            if t.value == 'return':
                return self.parse_return()
            if t.value == 'end':
                # stray end - consume and return noop
                self.advance()
                return None
        # fallback: expression statement
        expr = self.parse_expression()
        # consume optional NEWLINE
        if self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
        return {'type':'expr_stmt', 'expr': expr}

    def parse_let(self):
        self.expect(TokenType.KEYWORD, 'let')
        name = self.expect(TokenType.IDENT).value
        # optional '=' operator
        if self.peek() and self.peek().type == TokenType.OP and self.peek().value == '=':
            self.advance()
        # parse expression for the value
        if self.peek() and self.peek().type != TokenType.NEWLINE:
            value = self.parse_expression()
        else:
            value = None
        # consume NEWLINE
        if self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
        return Let(name, value)

    def parse_change(self):
        self.expect(TokenType.KEYWORD, 'change')
        name = self.expect(TokenType.IDENT).value
        # consume 'to' ident if present
        if self.peek() and self.peek().type == TokenType.IDENT and self.peek().value == 'to':
            self.advance()
        value = self.parse_expression()
        if self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
        return Change(name, value)

    def parse_if(self):
        self.expect(TokenType.KEYWORD, 'if')
        cond = self.parse_expression()
        # consume NEWLINE
        if self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
        body = self.parse_block()
        return If(cond, body)

    def parse_block(self):
        # expects INDENT then statements until DEDENT
        stmts = []
        if self.peek() and self.peek().type == TokenType.INDENT:
            self.advance()
            while self.peek() and self.peek().type != TokenType.DEDENT and self.peek().type != TokenType.EOF:
                if self.peek().type == TokenType.NEWLINE:
                    self.advance(); continue
                stmts.append(self.parse_statement())
            if self.peek() and self.peek().type == TokenType.DEDENT:
                self.advance()
        else:
            # single-line body (not indented)
            if self.peek() and self.peek().type != TokenType.NEWLINE:
                stmts.append(self.parse_statement())
                if self.peek() and self.peek().type == TokenType.NEWLINE:
                    self.advance()
        return stmts

    def parse_defi(self):
        # short function: defi name(params) => expr
        self.expect(TokenType.KEYWORD, 'defi')
        name = self.expect(TokenType.IDENT).value
        params = []
        if self.peek() and self.peek().type == TokenType.LPAREN:
            self.advance()
            while self.peek() and self.peek().type != TokenType.RPAREN:
                if self.peek().type == TokenType.COMMA:
                    self.advance(); continue
                if self.peek().type == TokenType.IDENT:
                    params.append(self.advance().value)
                else:
                    self.advance()
            if self.peek() and self.peek().type == TokenType.RPAREN:
                self.advance()
        # detect '=>' as two ops '=' '>' or a single OP
        # skip whitespace tokens; collect expression tokens until NEWLINE
        # if the next tokens are OP '=' then OP '>' consume them
        if self.peek() and self.peek().type == TokenType.OP and self.peek().value == '=':
            # lookahead for '>'
            self.advance()
            if self.peek() and self.peek().type == TokenType.OP and self.peek().value == '>':
                self.advance()
        # parse expression
        expr = self.parse_expression()
        if self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
        return Defi(name, params, expr)

    def parse_def(self):
        # block function: def name(params)
        self.expect(TokenType.KEYWORD, 'def')
        name = self.expect(TokenType.IDENT).value
        params = []
        if self.peek() and self.peek().type == TokenType.LPAREN:
            self.advance()
            while self.peek() and self.peek().type != TokenType.RPAREN:
                if self.peek().type == TokenType.COMMA:
                    self.advance(); continue
                if self.peek().type == TokenType.IDENT:
                    params.append(self.advance().value)
                else:
                    self.advance()
            if self.peek() and self.peek().type == TokenType.RPAREN:
                self.advance()
        # consume NEWLINE then parse indented block
        if self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
        body = self.parse_block()
        return FunctionDef(name, params, body)

    def parse_use(self):
        self.expect(TokenType.KEYWORD, 'use')
        name = self.expect(TokenType.IDENT).value
        if self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
        return Use(name)

    def parse_return(self):
        self.expect(TokenType.KEYWORD, 'return')
        if self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
            return Return(None)
        val = self.parse_expression()
        if self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
        return Return(val)

    def parse_expression(self):
        # Very small expression parser: handle binary + and identifiers/numbers/strings
        left = self.parse_primary()
        while self.peek() and self.peek().type == TokenType.OP and self.peek().value in ('+', '-', '*', '/', '>', '<', '=='):
            op = self.advance().value
            right = self.parse_primary()
            left = Binary(op, left, right)
        return left

    def parse_primary(self):
        t = self.peek()
        if not t:
            raise ParserError('Unexpected EOF')
        if t.type == TokenType.NUMBER:
            self.advance(); return Number(float(t.value) if '.' in t.value else int(t.value))
        if t.type == TokenType.STRING:
            self.advance(); return String(t.value)
        if t.type == TokenType.IDENT:
            # possible call
            ident = self.advance().value
            if self.peek() and self.peek().type == TokenType.LPAREN:
                self.advance()
                args = []
                while self.peek() and self.peek().type != TokenType.RPAREN:
                    if self.peek().type == TokenType.COMMA:
                        self.advance(); continue
                    args.append(self.parse_expression())
                if self.peek() and self.peek().type == TokenType.RPAREN:
                    self.advance()
                return Call(Ident(ident), args)
            return Ident(ident)
        # list literal using OP tokens '[' and ']'
        if t.type == TokenType.OP and t.value == '[':
            # consume '['
            self.advance()
            elements = []
            while self.peek() and not (self.peek().type == TokenType.OP and self.peek().value == ']'):
                if self.peek().type == TokenType.COMMA:
                    self.advance(); continue
                elements.append(self.parse_expression())
            # consume ']'
            if self.peek() and self.peek().type == TokenType.OP and self.peek().value == ']':
                self.advance()
            return ListLiteral(elements)
        if t.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            if self.peek() and self.peek().type == TokenType.RPAREN:
                self.advance()
            return expr
        raise ParserError(f'Unexpected token in primary: {t}')

if __name__ == '__main__':
    sample = '''let x = 5
if x > 0
    change x to 10
    defi add(a, b) => a + b
end
'''
    lex = Lexer(sample)
    toks = lex.tokenize()
    parser = Parser(toks)
    ast = parser.parse()
    import pprint
    pprint.pprint(ast)
