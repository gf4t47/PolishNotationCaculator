from interpreter.parser.node.sequence import Sequence
from src.interpreter.parser.node.node import AstNode
from src.interpreter.parser.node.binary import CalcOp, AssignOp
from src.interpreter.parser.node.factory import Num, Variable
from src.interpreter.visitor.enviroment import VariableEnviroment
from src.interpreter.visitor.node_visitor import NodeVisitor
from src.operators import calc_op_map


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Calculator(NodeVisitor):
    def __init__(self, tree: AstNode, env: VariableEnviroment):
        self._ast = tree
        self._env = env

    @property
    def ast_tree(self):
        return self._ast

    @property
    def _env(self):
        return self.__env

    @_env.setter
    def _env(self, val: VariableEnviroment):
        self.__env = val

    def visit_Num(self, node: Num)->int:
        return node.value

    def visit_Variable(self, node: Variable)->int:
        return self._env.lookup(node.name)

    def visit_CalcOp(self, node: CalcOp):
        op = node.op
        left_val = self.visit(node.left_expr)
        right_val = self.visit(node.right_expr)
        return calc_op_map[op.value](left_val, right_val)

    def visit_AssignOp(self, node: AssignOp):
        self._env.define(node.name, self.visit(node.value))
        return

    def visit_Sequence(self, node: Sequence):
        self._env = VariableEnviroment(prev=self._env)
        for p in node.preposition:
            self.visit(p)
        result = self.visit(node.action)
        self._env = self._env.previous
        return result

    def evaluate(self):
        return self.visit(self.ast_tree)
