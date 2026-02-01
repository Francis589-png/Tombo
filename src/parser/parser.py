"""
Parser for the Tombo language.
Converts token stream into an Abstract Syntax Tree (AST).
"""
from typing import List, Optional, Tuple
from lexer.token_types import Token, TokenType
from ast import *


class ParseError(Exception):
    """Raised when parser encounters an error."""

    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        line = token.line if token else "?"
        col = token.column if token else "?"
        super().__init__(f"{message} at line {line}, column {col}")


class Parser:
    """Parses Tombo token stream into AST."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None

    def error(self, message: str) -> None:
        """Raise a parse error."""
        raise ParseError(message, self.current_token)

    def peek(self, offset: int = 0) -> Optional[Token]:
        """Look ahead at a token without consuming."""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def advance(self) -> Token:
        """Consume and return the current token."""
        token = self.current_token
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
        return token

    def skip_newlines(self) -> None:
        """Skip any NEWLINE tokens."""
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()

    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        if not self.current_token:
            return False
        return self.current_token.type in types

    def consume(self, token_type: TokenType, message: str = None) -> Token:
        """Consume a token of a specific type or raise error."""
        if not self.match(token_type):
            self.error(message or f"Expected {token_type.name}")
        return self.advance()

    def parse(self) -> Program:
        """Parse the entire program."""
        statements = []
        self.skip_newlines()

        while self.current_token and self.current_token.type != TokenType.EOF:
            self.skip_newlines()
            if self.current_token and self.current_token.type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            self.skip_newlines()

        return Program(statements)

    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement."""
        self.skip_newlines()

        if not self.current_token or self.current_token.type == TokenType.EOF:
            return None

        # Check for dedent (end of block)
        if self.match(TokenType.DEDENT):
            return None

        # Variable declaration: let x = value
        if self.match(TokenType.LET):
            return self.parse_let_statement()

        # Variable assignment: change x to value
        if self.match(TokenType.CHANGE):
            return self.parse_change_statement()

        # Function definition: def name(params) block end
        if self.match(TokenType.DEF):
            return self.parse_function_def()

        # Shorthand function: defi name(params) => expression
        if self.match(TokenType.DEFI):
            return self.parse_shorthand_function_def()

        # If statement
        if self.match(TokenType.IF):
            return self.parse_if_statement()

        # While loop
        if self.match(TokenType.WHILE):
            return self.parse_while_loop()

        # For loop
        if self.match(TokenType.FOR):
            return self.parse_for_loop()

        # Match expression
        if self.match(TokenType.MATCH):
            return self.parse_match_statement()

        # Class definition
        if self.match(TokenType.CLASS):
            return self.parse_class_def()

        # Return statement
        if self.match(TokenType.RETURN):
            return self.parse_return_statement()

        # Break statement
        if self.match(TokenType.BREAK):
            self.advance()
            self.skip_newlines()
            return BreakStatement(self.current_token.line, self.current_token.column)

        # Continue statement
        if self.match(TokenType.CONTINUE):
            self.advance()
            self.skip_newlines()
            return ContinueStatement(self.current_token.line, self.current_token.column)

        # Try-except
        if self.match(TokenType.TRY):
            return self.parse_try_except()

        # Import statements
        if self.match(TokenType.IMPORT):
            return self.parse_import_statement()

        # Pass statement
        if self.match(TokenType.PASS):
            self.advance()
            self.skip_newlines()
            return PassStatement(self.current_token.line, self.current_token.column)

        # Otherwise, parse as expression statement
        expr = self.parse_expression()
        self.skip_newlines()
        return expr

    def parse_let_statement(self) -> VariableDecl:
        """Parse: let name = value."""
        token = self.consume(TokenType.LET)
        line, col = token.line, token.column

        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name after 'let'")
        name = name_token.value

        self.consume(TokenType.EQ, "Expected '=' after variable name")

        value = self.parse_expression()
        self.skip_newlines()

        return VariableDecl(name=name, value=value, mutable=False, line=line, column=col)

    def parse_change_statement(self) -> ChangeStatement:
        """Parse: change target to value."""
        token = self.consume(TokenType.CHANGE)
        line, col = token.line, token.column

        target = self.parse_postfix_expression()

        self.consume(TokenType.TO, "Expected 'to' after target in change statement")

        value = self.parse_expression()
        self.skip_newlines()

        return ChangeStatement(target=target, value=value, line=line, column=col)

    def parse_function_def(self) -> FunctionDef:
        """Parse: def name(params) block end."""
        token = self.consume(TokenType.DEF)
        line, col = token.line, token.column

        name_token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.value

        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        params = self.parse_parameters()
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")

        self.skip_newlines()

        # Parse function body (indented block)
        body = self.parse_block()

        # Optional: end keyword
        if self.match(TokenType.END):
            self.advance()

        self.skip_newlines()

        return FunctionDef(
            name=name, params=params, body=body, line=line, column=col
        )

    def parse_shorthand_function_def(self) -> ShorthandFunctionDef:
        """Parse: defi name(params) => expression."""
        token = self.consume(TokenType.DEFI)
        line, col = token.line, token.column

        name_token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.value

        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        params = self.parse_parameters()
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")

        self.consume(TokenType.ARROW, "Expected '=>' in shorthand function")

        body = self.parse_expression()
        self.skip_newlines()

        return ShorthandFunctionDef(
            name=name, params=params, body=body, line=line, column=col
        )

    def parse_if_statement(self) -> IfStatement:
        """Parse: if condition block [elif condition block] [else block]."""
        token = self.consume(TokenType.IF)
        line, col = token.line, token.column

        condition = self.parse_expression()
        self.skip_newlines()

        # Optional: then keyword
        if self.match(TokenType.THEN):
            self.advance()
            self.skip_newlines()

        then_block = self.parse_block()

        elif_blocks = []
        while self.match(TokenType.ELIF):
            self.advance()
            elif_condition = self.parse_expression()
            self.skip_newlines()
            elif_block = self.parse_block()
            elif_blocks.append((elif_condition, elif_block))

        else_block = None
        if self.match(TokenType.ELSE):
            self.advance()
            self.skip_newlines()
            else_block = self.parse_block()

        # Optional: end keyword
        if self.match(TokenType.END):
            self.advance()

        self.skip_newlines()

        return IfStatement(
            condition=condition,
            then_block=then_block,
            elif_blocks=elif_blocks,
            else_block=else_block,
            line=line,
            column=col,
        )

    def parse_while_loop(self) -> WhileLoop:
        """Parse: while condition block end."""
        token = self.consume(TokenType.WHILE)
        line, col = token.line, token.column

        condition = self.parse_expression()
        self.skip_newlines()

        body = self.parse_block()

        if self.match(TokenType.END):
            self.advance()

        self.skip_newlines()

        return WhileLoop(condition=condition, body=body, line=line, column=col)

    def parse_for_loop(self) -> ForLoop:
        """Parse: for variable in iterable block end."""
        token = self.consume(TokenType.FOR)
        line, col = token.line, token.column

        var_token = self.consume(TokenType.IDENTIFIER, "Expected variable in for loop")
        variable = var_token.value

        self.consume(TokenType.IN, "Expected 'in' in for loop")

        iterable = self.parse_expression()
        self.skip_newlines()

        body = self.parse_block()

        if self.match(TokenType.END):
            self.advance()

        self.skip_newlines()

        return ForLoop(
            variable=variable, iterable=iterable, body=body, line=line, column=col
        )

    def parse_match_statement(self) -> MatchExpr:
        """Parse: match value when pattern: expr [when pattern: expr] [else: expr]."""
        token = self.consume(TokenType.MATCH)
        line, col = token.line, token.column

        value = self.parse_expression()
        self.skip_newlines()

        cases = []
        default = None

        while self.match(TokenType.WHEN) or self.match(TokenType.ELSE):
            if self.match(TokenType.WHEN):
                self.advance()
                pattern = self.parse_expression()
                self.consume(TokenType.COLON, "Expected ':' after pattern")
                result = self.parse_expression()
                cases.append((pattern, result))
                self.skip_newlines()
            elif self.match(TokenType.ELSE):
                self.advance()
                self.consume(TokenType.COLON, "Expected ':' after 'else'")
                default = self.parse_expression()
                self.skip_newlines()

        return MatchExpr(value=value, cases=cases, default=default, line=line, column=col)

    def parse_class_def(self) -> ClassDef:
        """Parse: class Name block end."""
        token = self.consume(TokenType.CLASS)
        line, col = token.line, token.column

        name_token = self.consume(TokenType.IDENTIFIER, "Expected class name")
        name = name_token.value

        self.skip_newlines()

        # Parse class body
        methods = []
        body = []

        if self.match(TokenType.INDENT):
            self.advance()

            while self.current_token and not self.match(TokenType.DEDENT):
                self.skip_newlines()
                if self.match(TokenType.DEDENT):
                    break

                stmt = self.parse_statement()
                if stmt:
                    if isinstance(stmt, FunctionDef):
                        methods.append(stmt)
                    else:
                        body.append(stmt)

            if self.match(TokenType.DEDENT):
                self.advance()

        if self.match(TokenType.END):
            self.advance()

        self.skip_newlines()

        return ClassDef(name=name, methods=methods, body=body, line=line, column=col)

    def parse_return_statement(self) -> ReturnStatement:
        """Parse: return [value]."""
        token = self.consume(TokenType.RETURN)
        line, col = token.line, token.column

        value = None
        if not self.match(TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT):
            value = self.parse_expression()

        self.skip_newlines()

        return ReturnStatement(value=value, line=line, column=col)

    def parse_try_except(self) -> TryExcept:
        """Parse: try block catch [name] block [finally block]."""
        token = self.consume(TokenType.TRY)
        line, col = token.line, token.column

        self.skip_newlines()
        try_block = self.parse_block()

        catch_blocks = []
        while self.match(TokenType.CATCH):
            self.advance()

            # Optional error variable name
            error_name = None
            if self.match(TokenType.IDENTIFIER):
                error_name = self.current_token.value
                self.advance()

            self.skip_newlines()
            catch_body = self.parse_block()
            catch_blocks.append((None, error_name, catch_body))

        finally_block = None
        if self.match(TokenType.FINALLY):
            self.advance()
            self.skip_newlines()
            finally_block = self.parse_block()

        return TryExcept(
            try_block=try_block,
            catch_blocks=catch_blocks,
            finally_block=finally_block,
            line=line,
            column=col,
        )

    def parse_import_statement(self) -> ImportStatement:
        """Parse: import module [as alias]."""
        token = self.consume(TokenType.IMPORT)
        line, col = token.line, token.column

        module_token = self.consume(TokenType.IDENTIFIER, "Expected module name")
        module = module_token.value

        alias = None
        if self.match(TokenType.IDENTIFIER) and self.current_token.value == "as":
            self.advance()
            alias_token = self.consume(TokenType.IDENTIFIER)
            alias = alias_token.value

        self.skip_newlines()

        return ImportStatement(module=module, alias=alias, line=line, column=col)

    def parse_block(self) -> List[ASTNode]:
        """Parse an indented block of statements."""
        statements = []
        # Prefer indentation-based blocks when INDENT token is available
        if self.match(TokenType.INDENT):
            self.advance()  # Consume INDENT

            # Parse statements until DEDENT
            while self.current_token and not self.match(TokenType.DEDENT):
                self.skip_newlines()

                if self.match(TokenType.DEDENT):
                    break

                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)

            # Consume DEDENT
            if self.match(TokenType.DEDENT):
                self.advance()

            return statements

        # Fallback: accept non-indented blocks (useful for REPL input)
        # Parse statements until an explicit 'end', 'else', 'elif', DEDENT or EOF
        while self.current_token and not self.match(TokenType.END, TokenType.ELSE, TokenType.ELIF, TokenType.DEDENT, TokenType.EOF):
            self.skip_newlines()

            if self.match(TokenType.END, TokenType.ELSE, TokenType.ELIF, TokenType.DEDENT, TokenType.EOF):
                break

            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        return statements

    def parse_parameters(self) -> List[str]:
        """Parse function parameters: name, name, ..."""
        params = []

        while self.match(TokenType.IDENTIFIER):
            param_token = self.advance()
            params.append(param_token.value)

            if self.match(TokenType.COMMA):
                self.advance()
            else:
                break

        return params

    # =====================================================================
    # EXPRESSION PARSING
    # =====================================================================

    def parse_expression(self) -> ASTNode:
        """Parse an expression (handles operator precedence)."""
        return self.parse_ternary()

    def parse_ternary(self) -> ASTNode:
        """Parse: expr if condition else expr."""
        expr = self.parse_or()

        if self.match(TokenType.IF):
            self.advance()
            condition = self.parse_or()
            self.consume(TokenType.ELSE, "Expected 'else' in ternary expression")
            false_expr = self.parse_ternary()
            return TernaryExpr(
                condition=condition,
                true_value=expr,
                false_value=false_expr,
                line=expr.line,
                column=expr.column,
            )

        return expr

    def parse_or(self) -> ASTNode:
        """Parse: expr or expr or expr."""
        left = self.parse_and()

        while self.match(TokenType.OR):
            op_token = self.advance()
            right = self.parse_and()
            left = LogicalOp(
                left=left, operator="or", right=right, line=op_token.line, column=op_token.column
            )

        return left

    def parse_and(self) -> ASTNode:
        """Parse: expr and expr and expr."""
        left = self.parse_not()

        while self.match(TokenType.AND):
            op_token = self.advance()
            right = self.parse_not()
            left = LogicalOp(
                left=left, operator="and", right=right, line=op_token.line, column=op_token.column
            )

        return left

    def parse_not(self) -> ASTNode:
        """Parse: not expr."""
        if self.match(TokenType.NOT):
            op_token = self.advance()
            operand = self.parse_not()
            return UnaryOp(
                operator="not", operand=operand, line=op_token.line, column=op_token.column
            )

        return self.parse_comparison()

    def parse_comparison(self) -> ASTNode:
        """Parse: expr == expr, expr < expr, etc."""
        left = self.parse_bitwise_or()

        while self.match(
            TokenType.EQEQ,
            TokenType.NEQ,
            TokenType.LT,
            TokenType.GT,
            TokenType.LTE,
            TokenType.GTE,
        ):
            op_token = self.advance()
            right = self.parse_bitwise_or()
            left = BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column,
            )

        return left

    def parse_bitwise_or(self) -> ASTNode:
        """Parse: expr | expr."""
        left = self.parse_bitwise_xor()

        while self.match(TokenType.PIPE):
            op_token = self.advance()
            right = self.parse_bitwise_xor()
            left = BinaryOp(
                left=left,
                operator="|",
                right=right,
                line=op_token.line,
                column=op_token.column,
            )

        return left

    def parse_bitwise_xor(self) -> ASTNode:
        """Parse: expr ^ expr."""
        left = self.parse_bitwise_and()

        while self.match(TokenType.CARET):
            op_token = self.advance()
            right = self.parse_bitwise_and()
            left = BinaryOp(
                left=left,
                operator="^",
                right=right,
                line=op_token.line,
                column=op_token.column,
            )

        return left

    def parse_bitwise_and(self) -> ASTNode:
        """Parse: expr & expr."""
        left = self.parse_shift()

        while self.match(TokenType.AMPERSAND):
            op_token = self.advance()
            right = self.parse_shift()
            left = BinaryOp(
                left=left,
                operator="&",
                right=right,
                line=op_token.line,
                column=op_token.column,
            )

        return left

    def parse_shift(self) -> ASTNode:
        """Parse: expr << expr, expr >> expr."""
        left = self.parse_addition()

        while self.match(TokenType.LSHIFT, TokenType.RSHIFT):
            op_token = self.advance()
            right = self.parse_addition()
            left = BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column,
            )

        return left

    def parse_addition(self) -> ASTNode:
        """Parse: expr + expr, expr - expr."""
        left = self.parse_multiplication()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            right = self.parse_multiplication()
            left = BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column,
            )

        return left

    def parse_multiplication(self) -> ASTNode:
        """Parse: expr * expr, expr / expr, expr % expr."""
        left = self.parse_power()

        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_token = self.advance()
            right = self.parse_power()
            left = BinaryOp(
                left=left,
                operator=op_token.value,
                right=right,
                line=op_token.line,
                column=op_token.column,
            )

        return left

    def parse_power(self) -> ASTNode:
        """Parse: expr ** expr."""
        left = self.parse_unary()

        if self.match(TokenType.POWER):
            op_token = self.advance()
            right = self.parse_power()  # Right-associative
            left = BinaryOp(
                left=left,
                operator="**",
                right=right,
                line=op_token.line,
                column=op_token.column,
            )

        return left

    def parse_unary(self) -> ASTNode:
        """Parse: -expr, ~expr."""
        if self.match(TokenType.MINUS, TokenType.TILDE):
            op_token = self.advance()
            operand = self.parse_unary()
            return UnaryOp(
                operator=op_token.value,
                operand=operand,
                line=op_token.line,
                column=op_token.column,
            )

        return self.parse_postfix_expression()

    def parse_postfix_expression(self) -> ASTNode:
        """Parse: expr.property, expr[index], expr(args)."""
        expr = self.parse_primary()

        while True:
            # Member access: expr.property
            if self.match(TokenType.DOT):
                self.advance()
                property_token = self.consume(TokenType.IDENTIFIER, "Expected property name")
                property_name = property_token.value

                # Check if it's a method call
                if self.match(TokenType.LPAREN):
                    self.advance()
                    args = self.parse_arguments()
                    self.consume(TokenType.RPAREN)
                    expr = MethodCall(
                        object=expr,
                        method=property_name,
                        args=args,
                        line=property_token.line,
                        column=property_token.column,
                    )
                else:
                    expr = MemberAccess(
                        object=expr,
                        property=property_name,
                        line=property_token.line,
                        column=property_token.column,
                    )

            # Index access: expr[index]
            elif self.match(TokenType.LBRACKET):
                bracket_token = self.advance()
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET)
                expr = IndexExpr(
                    object=expr,
                    index=index,
                    line=bracket_token.line,
                    column=bracket_token.column,
                )

            # Function call: expr(args)
            elif self.match(TokenType.LPAREN):
                paren_token = self.advance()
                args = self.parse_arguments()
                self.consume(TokenType.RPAREN)
                expr = FunctionCall(
                    callee=expr,
                    args=args,
                    line=paren_token.line,
                    column=paren_token.column,
                )

            else:
                break

        return expr

    def parse_primary(self) -> ASTNode:
        """Parse primary expressions: literals, identifiers, parentheses."""
        token = self.current_token

        if not token:
            self.error("Unexpected end of input")

        # Number literal
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberLiteral(
                value=float(token.value), line=token.line, column=token.column
            )

        # String literal
        if token.type == TokenType.STRING:
            self.advance()
            return StringLiteral(
                value=token.value, line=token.line, column=token.column
            )

        # Boolean literal
        if token.type == TokenType.BOOLEAN:
            self.advance()
            value = token.value == "true"
            return BooleanLiteral(
                value=value, line=token.line, column=token.column
            )

        # Identifier
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(name=token.value, line=token.line, column=token.column)

        # Self reference
        if token.type == TokenType.SELF:
            self.advance()
            return SelfRef(line=token.line, column=token.column)

        # List literal: [1, 2, 3]
        if token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            while not self.match(TokenType.RBRACKET):
                elements.append(self.parse_expression())
                if self.match(TokenType.COMMA):
                    self.advance()
            self.consume(TokenType.RBRACKET)
            return ListLiteral(elements=elements, line=token.line, column=token.column)

        # Dictionary or set literal: {key: value} or {1, 2, 3}
        if token.type == TokenType.LBRACE:
            self.advance()

            # Empty dict/set
            if self.match(TokenType.RBRACE):
                self.advance()
                # Default to empty dict
                return DictLiteral(pairs=[], line=token.line, column=token.column)

            first = self.parse_expression()

            # Dictionary
            if self.match(TokenType.COLON):
                self.advance()
                value = self.parse_expression()
                pairs = [(first, value)]

                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.RBRACE):
                        break
                    key = self.parse_expression()
                    self.consume(TokenType.COLON)
                    val = self.parse_expression()
                    pairs.append((key, val))

                self.consume(TokenType.RBRACE)
                return DictLiteral(pairs=pairs, line=token.line, column=token.column)

            # Set
            else:
                elements = [first]
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.RBRACE):
                        break
                    elements.append(self.parse_expression())

                self.consume(TokenType.RBRACE)
                return SetLiteral(elements=elements, line=token.line, column=token.column)

        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')'")
            return expr

        # Lambda: => expr
        if token.type == TokenType.ARROW:
            self.advance()
            body = self.parse_expression()
            return LambdaExpr(params=[], body=body, line=token.line, column=token.column)

        self.error(f"Unexpected token: {token.type.name}")

    def parse_arguments(self) -> List[ASTNode]:
        """Parse function call arguments."""
        args = []

        while not self.match(TokenType.RPAREN):
            args.append(self.parse_expression())
            if self.match(TokenType.COMMA):
                self.advance()
            else:
                break

        return args
