from src.operators import calc_op_map
from src.interpreter.parser.node.sequence import Sequence
from src.interpreter.parser.node.node import AstNode
from src.interpreter.parser.node.binary import CalcOp, AssignOp
from src.interpreter.parser.node.factory import Num, Variable
from src.interpreter.visitor.environment import VariableEnvironment
from src.interpreter.visitor.node_visitor import NodeVisitor


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Calculator(NodeVisitor):
    def __init__(self, tree: AstNode, env: VariableEnvironment):
        self._ast = tree
        self.__env = env

    @property
    def ast_tree(self)->AstNode:
        return self._ast

    @property
    def _env(self)->VariableEnvironment:
        return self.__env

    def visit_Num(self, node: Num, env: VariableEnvironment)->int:
        return node.value

    def visit_Variable(self, node: Variable, env: VariableEnvironment)->int:
        found = env.lookup(node.name)
        if found is None:
            raise KeyError(f"Unresolved variable {node.name}")
        return found

    def visit_CalcOp(self, node: CalcOp, env: VariableEnvironment)->int:
        op = node.op
        left_val = self.visit(node.left_expr, env)
        right_val = self.visit(node.right_expr, env)
        return calc_op_map[op.value](left_val, right_val)

    def visit_AssignOp(self, node: AssignOp, env: VariableEnvironment)->None:
        env.define(node.name, self.visit(node.value, env))

    def visit_Sequence(self, node: Sequence, env: VariableEnvironment)->(int, AstNode):
        new_env = VariableEnvironment(prev=env)
        for p in node.preposition:
            self.visit(p, new_env)
        return self.visit(node.action, new_env)

    def evaluate(self):
        return self.visit(self.ast_tree, self._env)
