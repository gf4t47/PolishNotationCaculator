from interpreter.parser.node.node import AstNode


class NodeVisitor:
    def visit(self, node: AstNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name)
        return visitor(node)

    def generic_visit(self, node: AstNode):
        raise NotImplemented(f'{self.generic_visit.__name__} is not implemented yet')
