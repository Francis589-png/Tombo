"""
Tombo Language Interpreter
A universal interpreted programming language with indentation-based syntax.
"""

__version__ = "0.1.0"
__author__ = "Tombo Team"
__license__ = "MIT"

from src.lexer import Lexer, Token, TokenType
from src.parser import Parser
from src.ast import *


def run_code(source_code: str):
    """
    Run Tombo source code and return the result.
    
    Args:
        source_code: Tombo source code as string
        
    Returns:
        Execution result (to be implemented)
    """
    # Tokenize
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    # Parse
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Evaluate (to be implemented)
    # interpreter = Interpreter()
    # return interpreter.interpret(ast)
    
    return ast


__all__ = [
    "Lexer",
    "Parser",
    "Token",
    "TokenType",
    "Program",
    "run_code",
]
