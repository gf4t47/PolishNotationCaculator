from src.interpreter.parser.node.node import AstNode
from src.interpreter.visitor.environment import VariableEnvironment


class NodeVisitor:
    def visit(self, node: AstNode, env: VariableEnvironment):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name)
        return visitor(node, env)

    def generic_visit(self, node: AstNode, env: VariableEnvironment):
        raise NotImplemented(f'{self.generic_visit.__name__} is not implemented yet')
