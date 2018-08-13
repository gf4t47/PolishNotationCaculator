from src.interpreter.lexer.factory.operator_factory import operators
from src.interpreter.parser.node.node import AstNode


class Sequence(AstNode):
    def __init__(self, preposition: [AstNode], actor: [AstNode]):
        super().__init__(operators['='])
        self._preposition = preposition
        self._actor = actor

    @property
    def preposition(self):
        return self._preposition

    @property
    def action(self):
        return self._actor
