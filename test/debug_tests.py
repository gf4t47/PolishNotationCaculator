import pytest
from src.main import evaluate
from src.interpreter.lexer.token import Token, TokenType


@pytest.mark.parametrize("token", [Token(TokenType.NUMBER, 0)])
def test(token):
    print(token)
    assert token.type == TokenType.NUMBER
