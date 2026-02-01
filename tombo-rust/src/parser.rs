use crate::lexer::{Token, TokenType};
use crate::ast::{Expr, Stmt, Program, BinOp, UnOp};
use std::fmt;

#[derive(Debug)]
pub struct ParserError {
    pub message: String,
    pub line: usize,
    pub column: usize,
}

impl From<ParserError> for String {
    fn from(err: ParserError) -> String {
        err.message
    }
}

impl fmt::Display for ParserError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "Parser error at {}:{}: {}",
            self.line, self.column, self.message
        )
    }
}

impl std::error::Error for ParserError {}

pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Parser { tokens, pos: 0 }
    }

    pub fn parse(&mut self) -> Result<Program, ParserError> {
        let mut statements = Vec::new();

        while !self.is_at_end() {
            self.skip_newlines();
            if !self.is_at_end() {
                statements.push(self.parse_statement()?);
                self.skip_newlines();
            }
        }

        Ok(Program { statements })
    }

    fn parse_statement(&mut self) -> Result<Stmt, ParserError> {
        match &self.peek().token_type {
            TokenType::Let => self.parse_let(),
            TokenType::Change => self.parse_change(),
            TokenType::If => self.parse_if(),
            TokenType::While => self.parse_while(),
            TokenType::For => self.parse_for(),
            TokenType::Def => self.parse_fn(),
            TokenType::Return => self.parse_return(),
            TokenType::Break => {
                self.advance();
                Ok(Stmt::Break)
            }
            TokenType::Continue => {
                self.advance();
                Ok(Stmt::Continue)
            }
            TokenType::Pass => {
                self.advance();
                Ok(Stmt::Pass)
            }
            _ => {
                let expr = self.parse_expr()?;
                Ok(Stmt::Expr(expr))
            }
        }
    }

    fn parse_let(&mut self) -> Result<Stmt, ParserError> {
        self.consume_keyword("let")?;
        let name = self.parse_identifier()?;
        self.consume_token(TokenType::Equal)?;
        let value = self.parse_expr()?;
        Ok(Stmt::Let { name, value })
    }

    fn parse_change(&mut self) -> Result<Stmt, ParserError> {
        self.consume_keyword("change")?;
        let name = self.parse_identifier()?;
        self.consume_token(TokenType::To)?;
        let value = self.parse_expr()?;
        Ok(Stmt::Change { name, value })
    }

    fn parse_if(&mut self) -> Result<Stmt, ParserError> {
        self.consume_keyword("if")?;
        let condition = self.parse_expr()?;
        self.skip_newlines();
        self.consume_token(TokenType::Indent)?;
        let then_body = self.parse_block()?;
        self.consume_token(TokenType::Dedent)?;

        let mut elif_parts = Vec::new();
        let mut else_body = None;

        while self.match_keyword("elif") {
            let elif_cond = self.parse_expr()?;
            self.skip_newlines();
            self.consume_token(TokenType::Indent)?;
            let elif_body = self.parse_block()?;
            self.consume_token(TokenType::Dedent)?;
            elif_parts.push((elif_cond, elif_body));
        }

        if self.match_keyword("else") {
            self.skip_newlines();
            self.consume_token(TokenType::Indent)?;
            else_body = Some(self.parse_block()?);
            self.consume_token(TokenType::Dedent)?;
        }

        Ok(Stmt::If {
            condition,
            then_body,
            elif_parts,
            else_body,
        })
    }

    fn parse_while(&mut self) -> Result<Stmt, ParserError> {
        self.consume_keyword("while")?;
        let condition = self.parse_expr()?;
        self.skip_newlines();
        self.consume_token(TokenType::Indent)?;
        let body = self.parse_block()?;
        self.consume_token(TokenType::Dedent)?;
        Ok(Stmt::While { condition, body })
    }

    fn parse_for(&mut self) -> Result<Stmt, ParserError> {
        self.consume_keyword("for")?;
        let var = self.parse_identifier()?;
        self.consume_keyword("in")?;
        let iter = self.parse_expr()?;
        self.skip_newlines();
        self.consume_token(TokenType::Indent)?;
        let body = self.parse_block()?;
        self.consume_token(TokenType::Dedent)?;
        Ok(Stmt::For { var, iter, body })
    }

    fn parse_fn(&mut self) -> Result<Stmt, ParserError> {
        self.consume_keyword("def")?;
        let name = self.parse_identifier()?;
        self.consume_token(TokenType::LeftParen)?;
        let mut params = Vec::new();

        if !self.check(&TokenType::RightParen) {
            loop {
                params.push(self.parse_identifier()?);
                if !self.match_token(TokenType::Comma) {
                    break;
                }
            }
        }

        self.consume_token(TokenType::RightParen)?;
        self.skip_newlines();
        self.consume_token(TokenType::Indent)?;
        let body = self.parse_block()?;
        self.consume_token(TokenType::Dedent)?;

        Ok(Stmt::FnDef { name, params, body })
    }

    fn parse_return(&mut self) -> Result<Stmt, ParserError> {
        self.consume_keyword("return")?;
        let value = if self.check(&TokenType::Newline) || self.is_at_end() {
            None
        } else {
            Some(self.parse_expr()?)
        };
        Ok(Stmt::Return(value))
    }

    fn parse_block(&mut self) -> Result<Vec<Stmt>, ParserError> {
        let mut statements = Vec::new();

        while !self.check(&TokenType::Dedent) && !self.is_at_end() {
            self.skip_newlines();
            if !self.check(&TokenType::Dedent) && !self.is_at_end() {
                statements.push(self.parse_statement()?);
            }
        }

        Ok(statements)
    }

    fn parse_expr(&mut self) -> Result<Expr, ParserError> {
        self.parse_or()
    }

    fn parse_or(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_and()?;

        while self.match_keyword("or") {
            let right = self.parse_and()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op: BinOp::Or,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_and(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_not()?;

        while self.match_keyword("and") {
            let right = self.parse_not()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op: BinOp::And,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_not(&mut self) -> Result<Expr, ParserError> {
        if self.match_keyword("not") {
            let expr = self.parse_not()?;
            return Ok(Expr::UnaryOp {
                op: UnOp::Not,
                expr: Box::new(expr),
            });
        }

        self.parse_comparison()
    }

    fn parse_comparison(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_bitwise_or()?;

        loop {
            let op = match &self.peek().token_type {
                TokenType::DoubleEqual => BinOp::Equal,
                TokenType::NotEqual => BinOp::NotEqual,
                TokenType::Less => BinOp::Less,
                TokenType::Greater => BinOp::Greater,
                TokenType::LessEqual => BinOp::LessEqual,
                TokenType::GreaterEqual => BinOp::GreaterEqual,
                _ => break,
            };

            self.advance();
            let right = self.parse_bitwise_or()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_bitwise_or(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_bitwise_xor()?;

        while self.check(&TokenType::Pipe) && !self.peek_ahead().map_or(false, |t| {
            matches!(t.token_type, TokenType::Pipe)
        }) {
            self.advance();
            let right = self.parse_bitwise_xor()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op: BinOp::BitwiseOr,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_bitwise_xor(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_bitwise_and()?;

        while self.check(&TokenType::Caret) {
            self.advance();
            let right = self.parse_bitwise_and()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op: BinOp::BitwiseXor,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_bitwise_and(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_shift()?;

        while self.check(&TokenType::Ampersand)
            && !self.peek_ahead().map_or(false, |t| matches!(t.token_type, TokenType::Ampersand))
        {
            self.advance();
            let right = self.parse_shift()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op: BinOp::BitwiseAnd,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_shift(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_add()?;

        loop {
            let op = match &self.peek().token_type {
                TokenType::LeftShift => BinOp::LeftShift,
                TokenType::RightShift => BinOp::RightShift,
                _ => break,
            };

            self.advance();
            let right = self.parse_add()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_add(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_multiply()?;

        loop {
            let op = match &self.peek().token_type {
                TokenType::Plus => BinOp::Add,
                TokenType::Minus => BinOp::Subtract,
                _ => break,
            };

            self.advance();
            let right = self.parse_multiply()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_multiply(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_power()?;

        loop {
            let op = match &self.peek().token_type {
                TokenType::Star => BinOp::Multiply,
                TokenType::Slash => BinOp::Divide,
                TokenType::DoubleSlash => BinOp::FloorDivide,
                TokenType::Percent => BinOp::Modulo,
                _ => break,
            };

            self.advance();
            let right = self.parse_power()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_power(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_unary()?;

        if self.check(&TokenType::DoubleStar) {
            self.advance();
            let right = self.parse_power()?; // Right associative
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op: BinOp::Power,
                right: Box::new(right),
            };
        }

        Ok(expr)
    }

    fn parse_unary(&mut self) -> Result<Expr, ParserError> {
        match &self.peek().token_type {
            TokenType::Minus => {
                self.advance();
                let expr = self.parse_unary()?;
                Ok(Expr::UnaryOp {
                    op: UnOp::Negate,
                    expr: Box::new(expr),
                })
            }
            TokenType::Tilde => {
                self.advance();
                let expr = self.parse_unary()?;
                Ok(Expr::UnaryOp {
                    op: UnOp::BitwiseNot,
                    expr: Box::new(expr),
                })
            }
            _ => self.parse_postfix(),
        }
    }

    fn parse_postfix(&mut self) -> Result<Expr, ParserError> {
        let mut expr = self.parse_primary()?;

        loop {
            match &self.peek().token_type {
                TokenType::LeftParen => {
                    self.advance();
                    let mut args = Vec::new();

                    if !self.check(&TokenType::RightParen) {
                        loop {
                            args.push(self.parse_expr()?);
                            if !self.match_token(TokenType::Comma) {
                                break;
                            }
                        }
                    }

                    self.consume_token(TokenType::RightParen)?;
                    expr = Expr::Call {
                        func: Box::new(expr),
                        args,
                    };
                }
                TokenType::LeftBracket => {
                    self.advance();
                    let index = self.parse_expr()?;
                    self.consume_token(TokenType::RightBracket)?;
                    expr = Expr::Index {
                        object: Box::new(expr),
                        index: Box::new(index),
                    };
                }
                TokenType::Dot => {
                    self.advance();
                    let member = self.parse_identifier()?;
                    expr = Expr::Member {
                        object: Box::new(expr),
                        member,
                    };
                }
                _ => break,
            }
        }

        Ok(expr)
    }

    fn parse_primary(&mut self) -> Result<Expr, ParserError> {
        match &self.peek().token_type {
            TokenType::Integer(n) => {
                let val = *n;
                self.advance();
                Ok(Expr::Integer(val))
            }
            TokenType::Float(f) => {
                let val = *f;
                self.advance();
                Ok(Expr::Float(val))
            }
            TokenType::String(s) => {
                let val = s.clone();
                self.advance();
                Ok(Expr::String(val))
            }
            TokenType::Boolean(b) => {
                let val = *b;
                self.advance();
                Ok(Expr::Boolean(val))
            }
            TokenType::Identifier(name) => {
                let val = name.clone();
                self.advance();
                Ok(Expr::Identifier(val))
            }
            TokenType::LeftParen => {
                self.advance();
                let expr = self.parse_expr()?;
                self.consume_token(TokenType::RightParen)?;
                Ok(expr)
            }
            TokenType::LeftBracket => {
                self.advance();
                let mut elements = Vec::new();

                if !self.check(&TokenType::RightBracket) {
                    loop {
                        elements.push(self.parse_expr()?);
                        if !self.match_token(TokenType::Comma) {
                            break;
                        }
                    }
                }

                self.consume_token(TokenType::RightBracket)?;
                Ok(Expr::List(elements))
            }
            TokenType::LeftBrace => {
                self.advance();
                let mut pairs = Vec::new();

                if !self.check(&TokenType::RightBrace) {
                    loop {
                        let key = self.parse_expr()?;
                        self.consume_token(TokenType::Colon)?;
                        let value = self.parse_expr()?;
                        pairs.push((key, value));
                        if !self.match_token(TokenType::Comma) {
                            break;
                        }
                    }
                }

                self.consume_token(TokenType::RightBrace)?;
                Ok(Expr::Dict(pairs))
            }
            _ => Err(ParserError {
                message: format!("Unexpected token: {:?}", self.peek().token_type),
                line: self.peek().line,
                column: self.peek().column,
            }),
        }
    }

    // Helper methods
    fn peek(&self) -> Token {
        self.tokens
            .get(self.pos)
            .cloned()
            .unwrap_or(Token::new(TokenType::Eof, 0, 0))
    }

    fn peek_ahead(&self) -> Option<Token> {
        self.tokens.get(self.pos + 1).cloned()
    }

    fn advance(&mut self) {
        if !self.is_at_end() {
            self.pos += 1;
        }
    }

    fn is_at_end(&self) -> bool {
        matches!(self.peek().token_type, TokenType::Eof)
    }

    fn check(&self, token_type: &TokenType) -> bool {
        std::mem::discriminant(&self.peek().token_type) == std::mem::discriminant(token_type)
    }

    fn match_token(&mut self, token_type: TokenType) -> bool {
        if self.check(&token_type) {
            self.advance();
            true
        } else {
            false
        }
    }

    fn match_keyword(&mut self, keyword: &str) -> bool {
        // Accept either an Identifier token with the keyword string
        // or the dedicated keyword TokenType variant emitted by the lexer.
        if let TokenType::Identifier(name) = &self.peek().token_type {
            if name == keyword {
                self.advance();
                return true;
            }
        }

        if let Some(kw_token) = Self::keyword_token(keyword) {
            if self.check(&kw_token) {
                self.advance();
                return true;
            }
        }

        false
    }

    fn consume_token(&mut self, token_type: TokenType) -> Result<Token, ParserError> {
        if self.check(&token_type) {
            let token = self.peek();
            self.advance();
            Ok(token)
        } else {
            Err(ParserError {
                message: format!("Expected {:?}", token_type),
                line: self.peek().line,
                column: self.peek().column,
            })
        }
    }

    fn consume_keyword(&mut self, keyword: &str) -> Result<(), ParserError> {
        if let TokenType::Identifier(name) = &self.peek().token_type {
            if name == keyword {
                self.advance();
                return Ok(());
            }
        }

        if let Some(kw_token) = Self::keyword_token(keyword) {
            if self.check(&kw_token) {
                self.advance();
                return Ok(());
            }
        }

        Err(ParserError {
            message: format!("Expected '{}'", keyword),
            line: self.peek().line,
            column: self.peek().column,
        })
    }

    fn keyword_token(keyword: &str) -> Option<TokenType> {
        use crate::lexer::TokenType as KT;
        match keyword {
            "let" => Some(KT::Let),
            "change" => Some(KT::Change),
            "to" => Some(KT::To),
            "def" => Some(KT::Def),
            "if" => Some(KT::If),
            "else" => Some(KT::Else),
            "elif" => Some(KT::Elif),
            "for" => Some(KT::For),
            "while" => Some(KT::While),
            "in" => Some(KT::In),
            "return" => Some(KT::Return),
            "break" => Some(KT::Break),
            "continue" => Some(KT::Continue),
            "pass" => Some(KT::Pass),
            _ => None,
        }
    }

    fn parse_identifier(&mut self) -> Result<String, ParserError> {
        if let TokenType::Identifier(name) = &self.peek().token_type {
            let val = name.clone();
            self.advance();
            Ok(val)
        } else {
            Err(ParserError {
                message: "Expected identifier".to_string(),
                line: self.peek().line,
                column: self.peek().column,
            })
        }
    }

    fn skip_newlines(&mut self) {
        while self.check(&TokenType::Newline) {
            self.advance();
        }
    }
}
