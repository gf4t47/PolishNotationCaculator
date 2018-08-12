from src.calculator import op_calc_map
from src.interpreter.parser.node.binary import BinaryOp
from src.interpreter.parser.node.factory import Num
from src.interpreter.visitor.node_visitor import NodeVisitor


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Calculator(NodeVisitor):
    def __init__(self, tree):
        self._ast = tree

    @property
    def ast_tree(self):
        return self._ast

    def visit_Num(self, node: Num)->int:
        return node.value

    def visit_BinaryOp(self, node: BinaryOp):
        op = node.op
        left_val = self.visit(node.left_expr)
        right_val = self.visit(node.right_expr)
        return op_calc_map[op.value](left_val, right_val)

    def evaluate(self):
        return self.visit(self.ast_tree)
