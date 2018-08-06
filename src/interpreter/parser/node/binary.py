from src.interpreter.lexer.token import Token, TokenType
from src.interpreter.parser.node.node import AstNode


class BinaryOp(AstNode):
    def __init__(self, op: Token, left: AstNode, right: AstNode):
        assert op.type == TokenType.OPERATOR
        super().__init__(op)
        self._left = left
        self._right = right

    def __str__(self):
        return str(f'({self.op.value} {self.left_expr} {self.right_expr})')

    @property
    def op(self)-> Token:
        return self.token

    @property
    def left_expr(self)-> AstNode:
        return self._left

    @property
    def right_expr(self)-> AstNode:
        return self._right
