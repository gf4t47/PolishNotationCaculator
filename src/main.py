from src.stack.stack_interpreter import StackInterpreter


def evaluate(expression: str, free_op: bool) -> int:
    """
    :type free_op: bool
    :param free_op: indicate whether the calculator support free operator (operator can operate operands number larger than 2)
    :type expression: str
    :param expression: input expression
    :rtype: int
    :return: evaluated value for the input expression
    """
    return StackInterpreter(free_op).evaluate(expression)
