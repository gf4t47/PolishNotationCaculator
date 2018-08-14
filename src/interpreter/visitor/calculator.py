from src.interpreter.parser.node.sequence import Sequence
from src.interpreter.parser.node.node import AstNode
from src.interpreter.parser.node.binary import CalcOp, AssignOp
from src.interpreter.parser.node.factory import Num, Variable
from src.interpreter.visitor.environment import VariableEnvironment
from src.interpreter.visitor.node_visitor import NodeVisitor
from src.operators import calc


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Calculator(NodeVisitor):
    def __init__(self, tree: AstNode, env: VariableEnvironment):
        self._ast = tree
        self.__env = env

    @property
    def ast_tree(self):
        return self._ast

    @property
    def _env(self):
        return self.__env

    def visit_Num(self, node: Num, env: VariableEnvironment)->int:
        return node.value

    def visit_Variable(self, node: Variable, env: VariableEnvironment)->int:
        found = env.lookup(node.name)
        return found if found is not None else node

    def visit_CalcOp(self, node: CalcOp, env: VariableEnvironment):
        op = node.op
        left_val = self.visit(node.left_expr, env)
        right_val = self.visit(node.right_expr, env)
        return calc(op, left_val, right_val)

    def visit_AssignOp(self, node: AssignOp, env: VariableEnvironment):
        env.define(node.name, self.visit(node.value, env))
        return

    def visit_Sequence(self, node: Sequence, env: VariableEnvironment):
        new_env = VariableEnvironment(prev=env)
        for p in node.preposition:
            self.visit(p, new_env)
        return self.visit(node.action, new_env)

    def evaluate(self):
        return self.visit(self.ast_tree, self._env)
