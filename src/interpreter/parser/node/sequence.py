from src.interpreter.lexer.token import Token
from src.interpreter.lexer.factory.operator_factory import operators
from src.interpreter.parser.node.node import AstNode, OpNode


class Sequence(AstNode):
    def __init__(self, preposition: [AstNode], actor: AstNode):
        super().__init__(operators['='])
        self._preposition = preposition
        self._actor = actor

    @property
    def preposition(self)->[AstNode]:
        return self._preposition

    @property
    def action(self)->AstNode:
        return self._actor


class CalcMultiple(OpNode):
    def __init__(self, op: Token, operands: [AstNode]):
        super().__init__(op)
        self._operands = operands

    @property
    def operands(self):
        return self._operands
