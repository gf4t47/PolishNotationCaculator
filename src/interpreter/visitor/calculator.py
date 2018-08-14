from src.interpreter.parser.node.sequence import Sequence
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
        self.__env = env

    @property
    def ast_tree(self):
        return self._ast

    @property
    def _env(self):
        return self.__env

    def visit_Num(self, node: Num, env: VariableEnviroment)->int:
        return node.value

    def visit_Variable(self, node: Variable, env: VariableEnviroment)->int:
        return env.lookup(node.name)

    def visit_CalcOp(self, node: CalcOp, env: VariableEnviroment):
        op = node.op
        left_val = self.visit(node.left_expr, env)
        right_val = self.visit(node.right_expr, env)
        return calc_op_map[op.value](left_val, right_val)

    def visit_AssignOp(self, node: AssignOp, env: VariableEnviroment):
        env.define(node.name, self.visit(node.value, env))
        return

    def visit_Sequence(self, node: Sequence, env: VariableEnviroment):
        new_env = VariableEnviroment(prev=env)
        for p in node.preposition:
            self.visit(p, new_env)
        return self.visit(node.action, new_env)

    def evaluate(self):
        return self.visit(self.ast_tree, self._env)
