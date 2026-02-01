use super::{Token, TokenType, LexerError};

pub struct Lexer {
    source: Vec<char>,
    pos: usize,
    line: usize,
    column: usize,
    indent_stack: Vec<usize>,
}

impl Lexer {
    pub fn new(source: &str) -> Self {
        Lexer {
            source: source.chars().collect(),
            pos: 0,
            line: 1,
            column: 0,
            indent_stack: vec![0],
        }
    }

    pub fn tokenize(&mut self) -> Result<Vec<Token>, LexerError> {
        let mut tokens = Vec::new();

        // Handle initial indentation
        self.handle_line_start(&mut tokens)?;

        while self.pos < self.source.len() {
            self.skip_whitespace_inline();

            let ch = match self.peek() {
                Some(c) => c,
                None => break,
            };

            // Comments
            if ch == '#' {
                self.skip_comment();
                continue;
            }

            // Newlines
            if ch == '\n' {
                tokens.push(Token::new(TokenType::Newline, self.line, self.column));
                self.advance();
                self.line += 1;
                self.column = 0;
                self.handle_line_start(&mut tokens)?;
                continue;
            }

            // String literals
            if ch == '"' || ch == '\'' {
                tokens.push(self.read_string()?);
                continue;
            }

            // Numbers
            if ch.is_ascii_digit() {
                tokens.push(self.read_number()?);
                continue;
            }

            // Identifiers and keywords
            if ch.is_alphabetic() || ch == '_' {
                tokens.push(self.read_identifier());
                continue;
            }

            // Operators and delimiters
            tokens.push(self.read_operator()?);
        }

        // Handle final dedents
        while self.indent_stack.len() > 1 {
            self.indent_stack.pop();
            tokens.push(Token::new(TokenType::Dedent, self.line, self.column));
        }

        tokens.push(Token::new(TokenType::Eof, self.line, self.column));
        Ok(tokens)
    }

    fn peek(&self) -> Option<char> {
        self.source.get(self.pos).copied()
    }

    fn peek_next(&self) -> Option<char> {
        self.source.get(self.pos + 1).copied()
    }

    fn handle_line_start(&mut self, tokens: &mut Vec<Token>) -> Result<(), LexerError> {
        let mut indent = 0;

        while self.pos < self.source.len() && self.source[self.pos] == ' ' {
            indent += 1;
            self.advance();
        }

        // Skip empty lines and comments
        if self.pos >= self.source.len()
            || self.source[self.pos] == '\n'
            || self.source[self.pos] == '#'
        {
            return Ok(());
        }

        let current_indent = *self.indent_stack.last().unwrap();

        if indent > current_indent {
            self.indent_stack.push(indent);
            tokens.push(Token::new(TokenType::Indent, self.line, self.column));
        } else if indent < current_indent {
            while let Some(&stack_indent) = self.indent_stack.last() {
                if stack_indent <= indent {
                    break;
                }
                self.indent_stack.pop();
                tokens.push(Token::new(TokenType::Dedent, self.line, self.column));
            }

            if self.indent_stack.last() != Some(&indent) {
                return Err(LexerError {
                    message: "Indentation error".to_string(),
                    line: self.line,
                    column: self.column,
                });
            }
        }

        Ok(())
    }

    fn read_identifier(&mut self) -> Token {
        let start_line = self.line;
        let start_col = self.column;
        let mut ident = String::new();

        while self.pos < self.source.len()
            && (self.source[self.pos].is_alphanumeric() || self.source[self.pos] == '_')
        {
            ident.push(self.source[self.pos]);
            self.advance();
        }

        let token_type = match ident.as_str() {
            "let" => TokenType::Let,
            "change" => TokenType::Change,
            "to" => TokenType::To,
            "def" => TokenType::Def,
            "if" => TokenType::If,
            "else" => TokenType::Else,
            "elif" => TokenType::Elif,
            "for" => TokenType::For,
            "while" => TokenType::While,
            "in" => TokenType::In,
            "end" => TokenType::End,
            "return" => TokenType::Return,
            "match" => TokenType::Match,
            "when" => TokenType::When,
            "class" => TokenType::Class,
            "self" => TokenType::Self_,
            "import" => TokenType::Import,
            "use" => TokenType::Use,
            "try" => TokenType::Try,
            "catch" => TokenType::Catch,
            "finally" => TokenType::Finally,
            "async" => TokenType::Async,
            "await" => TokenType::Await,
            "break" => TokenType::Break,
            "continue" => TokenType::Continue,
            "pass" => TokenType::Pass,
            "then" => TokenType::Then,
            "true" => TokenType::Boolean(true),
            "false" => TokenType::Boolean(false),
            "and" => TokenType::And,
            "or" => TokenType::Or,
            "not" => TokenType::Not,
            _ => TokenType::Identifier(ident),
        };

        Token::new(token_type, start_line, start_col)
    }

    fn read_string(&mut self) -> Result<Token, LexerError> {
        let start_line = self.line;
        let start_col = self.column;
        let quote = match self.peek() {
            Some(q) => q,
            None => {
                return Err(LexerError {
                    message: "Unterminated string".to_string(),
                    line: start_line,
                    column: start_col,
                })
            }
        };
        self.advance(); // Skip opening quote

        let mut value = String::new();

        loop {
            let curr = match self.peek() {
                Some(c) => c,
                None => break,
            };

            if curr == quote {
                break;
            }

            if curr == '\\' {
                // escape sequence
                // ensure there's a next char
                if let Some(_) = self.peek_next() {
                    self.advance(); // consume backslash
                    let esc = match self.peek() {
                        Some(c) => c,
                        None => {
                            return Err(LexerError {
                                message: "Unterminated string".to_string(),
                                line: start_line,
                                column: start_col,
                            })
                        }
                    };
                    value.push(match esc {
                        'n' => '\n',
                        't' => '\t',
                        'r' => '\r',
                        '\\' => '\\',
                        '\'' => '\'',
                        '"' => '"',
                        other => other,
                    });
                    self.advance(); // consume escaped char
                    continue;
                } else {
                    return Err(LexerError {
                        message: "Unterminated string".to_string(),
                        line: start_line,
                        column: start_col,
                    });
                }
            }

            // regular character
            value.push(curr);
            self.advance();
        }

        if self.pos >= self.source.len() {
            return Err(LexerError {
                message: "Unterminated string".to_string(),
                line: start_line,
                column: start_col,
            });
        }

        self.advance(); // Skip closing quote
        Ok(Token::new(TokenType::String(value), start_line, start_col))
    }

    fn read_number(&mut self) -> Result<Token, LexerError> {
        let start_line = self.line;
        let start_col = self.column;
        let mut num_str = String::new();
        let mut is_float = false;

        while self.pos < self.source.len()
            && (self.source[self.pos].is_ascii_digit() || self.source[self.pos] == '.')
        {
            if self.source[self.pos] == '.' {
                if is_float {
                    break;
                }
                is_float = true;
            }
            num_str.push(self.source[self.pos]);
            self.advance();
        }

        let token_type = if is_float {
            TokenType::Float(num_str.parse().unwrap())
        } else {
            TokenType::Integer(num_str.parse().unwrap())
        };

        Ok(Token::new(token_type, start_line, start_col))
    }

    fn read_operator(&mut self) -> Result<Token, LexerError> {
        let start_line = self.line;
        let start_col = self.column;
        let ch = self.source[self.pos];

        let token_type = match ch {
            '+' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::PlusEqual
                } else {
                    TokenType::Plus
                }
            }
            '-' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::MinusEqual
                } else if self.pos < self.source.len() && self.source[self.pos] == '>' {
                    self.advance();
                    TokenType::Arrow
                } else {
                    TokenType::Minus
                }
            }
            '*' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '*' {
                    self.advance();
                    if self.pos < self.source.len() && self.source[self.pos] == '=' {
                        self.advance();
                        TokenType::DoubleStarEqual
                    } else {
                        TokenType::DoubleStar
                    }
                } else if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::StarEqual
                } else {
                    TokenType::Star
                }
            }
            '/' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '/' {
                    self.advance();
                    if self.pos < self.source.len() && self.source[self.pos] == '=' {
                        self.advance();
                        TokenType::DoubleSlashEqual
                    } else {
                        TokenType::DoubleSlash
                    }
                } else if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::SlashEqual
                } else {
                    TokenType::Slash
                }
            }
            '%' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::PercentEqual
                } else {
                    TokenType::Percent
                }
            }
            '=' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::DoubleEqual
                } else if self.pos < self.source.len() && self.source[self.pos] == '>' {
                    self.advance();
                    TokenType::FatArrow
                } else {
                    TokenType::Equal
                }
            }
            '!' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::NotEqual
                } else {
                    return Err(LexerError {
                        message: "Unexpected character '!'".to_string(),
                        line: start_line,
                        column: start_col,
                    });
                }
            }
            '<' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::LessEqual
                } else if self.pos < self.source.len() && self.source[self.pos] == '<' {
                    self.advance();
                    if self.pos < self.source.len() && self.source[self.pos] == '=' {
                        self.advance();
                        TokenType::LeftShiftEqual
                    } else {
                        TokenType::LeftShift
                    }
                } else {
                    TokenType::Less
                }
            }
            '>' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::GreaterEqual
                } else if self.pos < self.source.len() && self.source[self.pos] == '>' {
                    self.advance();
                    if self.pos < self.source.len() && self.source[self.pos] == '=' {
                        self.advance();
                        TokenType::RightShiftEqual
                    } else {
                        TokenType::RightShift
                    }
                } else {
                    TokenType::Greater
                }
            }
            '&' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '&' {
                    self.advance();
                    TokenType::DoubleAmpersand
                } else if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::AmpersandEqual
                } else {
                    TokenType::Ampersand
                }
            }
            '|' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '|' {
                    self.advance();
                    TokenType::DoublePipe
                } else if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::PipeEqual
                } else {
                    TokenType::Pipe
                }
            }
            '^' => {
                self.advance();
                if self.pos < self.source.len() && self.source[self.pos] == '=' {
                    self.advance();
                    TokenType::CaretEqual
                } else {
                    TokenType::Caret
                }
            }
            '~' => {
                self.advance();
                TokenType::Tilde
            }
            '(' => {
                self.advance();
                TokenType::LeftParen
            }
            ')' => {
                self.advance();
                TokenType::RightParen
            }
            '[' => {
                self.advance();
                TokenType::LeftBracket
            }
            ']' => {
                self.advance();
                TokenType::RightBracket
            }
            '{' => {
                self.advance();
                TokenType::LeftBrace
            }
            '}' => {
                self.advance();
                TokenType::RightBrace
            }
            ',' => {
                self.advance();
                TokenType::Comma
            }
            ':' => {
                self.advance();
                TokenType::Colon
            }
            ';' => {
                self.advance();
                TokenType::Semicolon
            }
            '.' => {
                self.advance();
                TokenType::Dot
            }
            '?' => {
                self.advance();
                TokenType::Question
            }
            _ => {
                return Err(LexerError {
                    message: format!("Unexpected character '{}'", ch),
                    line: start_line,
                    column: start_col,
                });
            }
        };

        Ok(Token::new(token_type, start_line, start_col))
    }

    fn skip_whitespace_inline(&mut self) {
        while self.pos < self.source.len() && self.source[self.pos] == ' ' {
            self.advance();
        }
    }

    fn skip_comment(&mut self) {
        while self.pos < self.source.len() && self.source[self.pos] != '\n' {
            self.advance();
        }
    }

    fn advance(&mut self) {
        if self.pos < self.source.len() {
            if self.source[self.pos] == '\n' {
                self.line += 1;
                self.column = 0;
            } else {
                self.column += 1;
            }
            self.pos += 1;
        }
    }
}
