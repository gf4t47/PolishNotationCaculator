from src.interpreter.parser.node.factory import Variable
from src.interpreter.lexer.token import Token, TokenType
from src.interpreter.parser.node.node import AstNode


class BinaryOp(AstNode):
    def __init__(self, op: Token, left: AstNode, right: AstNode):
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


class CalcOp(BinaryOp):
    def __init__(self, op: Token, left: AstNode, right: AstNode):
        assert op.type == TokenType.CALCULATOR
        super().__init__(op, left, right)


class AssignOp(BinaryOp):
    def __init__(self, op: Token, left: Variable, right: AstNode):
        assert op.type == TokenType.ASSIGN
        super().__init__(op, left, right)

    @property
    def name(self)->str:
        return self.left_expr.name

    @property
    def value(self):
        return self.right_expr
