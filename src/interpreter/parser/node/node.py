from src.interpreter.lexer.token import Token, TokenType


class AstNode:
    def __init__(self, token: Token):
        self._token = token

    @property
    def token(self)-> Token:
        return self._token

    @property
    def type(self)-> TokenType:
        return self.token.type
