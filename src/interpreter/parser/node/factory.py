from src.interpreter.lexer.token import Token, TokenType
from src.interpreter.parser.node.node import AstNode


class FactorNode(AstNode):
    def __str__(self):
        return str(self.value)

    @property
    def value(self)->(int, str, bool):
        return self.token.value


class Num(FactorNode):
    def __init__(self, token: Token):
        assert token.type == TokenType.NUMBER
        super().__init__(token)
