import pytest

from src.interpreter.input.string_stream import MovableStream
from src.interpreter.lexer.lexer import Lexer
from src.interpreter.lexer.factory.bracket_factory import brackets
from src.interpreter.lexer.factory.operator_factory import operators
from src.interpreter.lexer.token import Token, TokenType
from src.interpreter.parser.token_stream import TokenStream


def tokenize(expr: str)-> [Token]:
    str_stream = MovableStream(expr)
    lexer = Lexer(str_stream)
    token_stream = TokenStream(lexer)

    result = []
    cur_token = token_stream.next_token()

    while cur_token.type != TokenType.EOF:
        result.append(cur_token)
        cur_token = token_stream.next_token()

    return result


@pytest.mark.parametrize("bracket, expected", [
    ('(', [brackets['(']]),
    (')', [brackets[')']]),
    (' ()', [brackets['('], brackets[')']]),
    (') (', [brackets[')'], brackets['(']]),
])
def test_bracket(bracket, expected):
    assert expected == tokenize(bracket)


@pytest.mark.parametrize("operator, expected", [
    ('+', [operators['+']]),
    ('-', [operators['-']]),
    ('*', [operators['*']]),
    ('/', [operators['/']]),
    ('+ +', [operators['+'], operators['+']]),
    ('-  -', [operators['-'], operators['-']]),
    ('**', [operators['*'], operators['*']]),
    ('//', [operators['/'], operators['/']]),
])
def test_operators(operator, expected):
    assert expected == tokenize(operator)


@pytest.mark.parametrize("number, expected", [
    ('001', [Token(TokenType.NUMBER, 1)]),
    ('0', [Token(TokenType.NUMBER, 0)]),
    ('-1', [Token(TokenType.NUMBER, -1)]),
    ('-01', [Token(TokenType.NUMBER, -1)]),
    ('-10', [Token(TokenType.NUMBER, -10)]),
    ('0100', [Token(TokenType.NUMBER, 100)]),
    ('0 21 100', [Token(TokenType.NUMBER, 0), Token(TokenType.NUMBER, 21), Token(TokenType.NUMBER, 100)]),
])
def test_number(number, expected):
    assert expected == tokenize(str(number))


@pytest.mark.parametrize("expr, expected", [
    ('1 + 1', [Token(TokenType.NUMBER, 1), operators['+'], Token(TokenType.NUMBER, 1)]),
    ('0 / * 0', [Token(TokenType.NUMBER, 0), operators['/'], operators['*'], Token(TokenType.NUMBER, 0)]),
    ('100 - 22 / 34', [Token(TokenType.NUMBER, 100), operators['-'], Token(TokenType.NUMBER, 22), operators['/'], Token(TokenType.NUMBER, 34)]),
    ('121 09 ** 12', [Token(TokenType.NUMBER, 121), Token(TokenType.NUMBER, 9),operators['*'], operators['*'], Token(TokenType.NUMBER, 12)]),
])
def test_number_operator(expr, expected):
    assert expected == tokenize(expr)


@pytest.mark.parametrize("expr, expected", [
    ('( 1 + 1 )', [brackets['('], Token(TokenType.NUMBER, 1), operators['+'], Token(TokenType.NUMBER, 1), brackets[')']]),
    ('0 / (* 0)', [Token(TokenType.NUMBER, 0), operators['/'], brackets['('], operators['*'], Token(TokenType.NUMBER, 0), brackets[')']]),
    ('100 - (22 / 34)', [Token(TokenType.NUMBER, 100), operators['-'], brackets['('], Token(TokenType.NUMBER, 22), operators['/'], Token(TokenType.NUMBER, 34), brackets[')']]),
    ('((121 09) ** 12)', [brackets['('], brackets['('], Token(TokenType.NUMBER, 121), Token(TokenType.NUMBER, 9), brackets[')'], operators['*'], operators['*'], Token(TokenType.NUMBER, 12), brackets[')']]),
])
def test_number_op_bracket(expr, expected):
    assert expected == tokenize(expr)
