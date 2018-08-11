import pytest

from src.interpreter.input.string_stream import MovableStream
from src.interpreter.lexer.lexer import Lexer
from src.interpreter.parser.token_stream import TokenStream
from src.interpreter.parser.parser import Parser


def test():
    string = MovableStream('+ 1 1 1')
    lexer = Lexer(string)
    tokens = TokenStream(lexer)
    parser = Parser(tokens, False)
    ast = parser.parse()
    print(ast)
    assert ast is not None

