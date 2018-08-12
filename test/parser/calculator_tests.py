import pytest

from src.interpreter.visitor.calculator import Calculator
from src.interpreter.input.string_stream import MovableStream
from src.interpreter.lexer.lexer import Lexer
from src.interpreter.parser.token_stream import TokenStream
from src.interpreter.parser.parser import Parser


@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('( 1 )', 1),
    ('(( 1 ))', 1),
    ('+ 1 1', 2),
    ('( + 1 1 )', 2),
    ('+ 1 1 1', 3),
    ('( + 1 1 1 )', 3),
    ('+ 1 ( + 1 1 1 )', 4),
    ('(((( + 1 ( + 1 1 1 )))))', 4),
])
def test(expr, expected):
    string = MovableStream(expr)
    lexer = Lexer(string)
    tokens = TokenStream(lexer)
    parser = Parser(tokens, False)
    ast = parser.parse()
    calculator = Calculator(ast)
    assert expected == calculator.evaluate()

