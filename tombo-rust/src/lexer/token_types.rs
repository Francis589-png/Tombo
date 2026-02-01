use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {
    // Literals
    Integer(i64),
    Float(f64),
    String(String),
    Boolean(bool),

    // Keywords
    Let,
    Change,
    To,
    Def,
    If,
    Else,
    Elif,
    For,
    While,
    In,
    End,
    Return,
    Match,
    When,
    Class,
    Self_,
    Import,
    Use,
    Try,
    Catch,
    Finally,
    Async,
    Await,
    Break,
    Continue,
    Pass,
    Then,
    And,
    Or,
    Not,

    // Operators
    Plus,
    Minus,
    Star,
    Slash,
    Percent,
    DoubleSlash,
    DoubleStar,
    Equal,
    DoubleEqual,
    NotEqual,
    Less,
    Greater,
    LessEqual,
    GreaterEqual,
    Ampersand,
    Pipe,
    Caret,
    Tilde,
    DoubleAmpersand,
    DoublePipe,
    PlusEqual,
    MinusEqual,
    StarEqual,
    SlashEqual,
    DoubleSlashEqual,
    PercentEqual,
    DoubleStarEqual,
    AmpersandEqual,
    PipeEqual,
    CaretEqual,
    LeftShift,
    RightShift,
    LeftShiftEqual,
    RightShiftEqual,

    // Delimiters
    LeftParen,
    RightParen,
    LeftBracket,
    RightBracket,
    LeftBrace,
    RightBrace,
    Comma,
    Colon,
    Semicolon,
    Dot,
    Arrow,
    FatArrow,
    Question,

    // Special
    Indent,
    Dedent,
    Newline,
    Eof,

    // Identifiers
    Identifier(String),
}

#[derive(Debug, Clone)]
pub struct Token {
    pub token_type: TokenType,
    pub line: usize,
    pub column: usize,
}

impl Token {
    pub fn new(token_type: TokenType, line: usize, column: usize) -> Self {
        Token {
            token_type,
            line,
            column,
        }
    }
}

#[derive(Debug)]
pub struct LexerError {
    pub message: String,
    pub line: usize,
    pub column: usize,
}

impl fmt::Display for LexerError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "Lexer error at {}:{}: {}",
            self.line, self.column, self.message
        )
    }
}

impl std::error::Error for LexerError {}
