import pytest

from src.interpreter.input.string_stream import MovableStream
from src.interpreter.lexer.lexer import Lexer
from src.interpreter.parser.token_stream import TokenStream
from src.interpreter.parser.parser import Parser


def test():
    string = MovableStream('2')
    lexer = Lexer(string)
    tokens = TokenStream(lexer)
    p = Parser(tokens)

    valid, token = p._syntax_error_wrapper(p.number)
    print(token)
    assert True == valid

