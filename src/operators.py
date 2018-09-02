import operator

from src.interpreter.parser.node.binary import CalcBinary
from src.interpreter.lexer.token import Token
from src.interpreter.parser.node.node import AstNode

calc_op_map = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv
}


def simplify(op: Token, node: AstNode, val: int):
    pass


def calc_node(op: Token, left: (int, AstNode), right: (int, AstNode)) -> (int, AstNode):
    if type(left) is int and type(right) is int:
        return calc_op_map[op.value](left, right)
    elif isinstance(left, AstNode) and isinstance(right, AstNode):
        return CalcBinary(op, left, right)
    elif type(left) is int:
        pass
    elif type(right) is int:
        pass

    raise NotImplemented('not yet')
