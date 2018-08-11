from src.interpreter.input.string_stream import MovableStream
from src.interpreter.lexer.lexer import Lexer
from src.interpreter.parser.token_stream import TokenStream
from src.interpreter.parser.parser import Parser

from src.stack.stack_interpreter import StackInterpreter


def evaluate_stack(expression: str, binary_op: bool) -> int:
    """
    :type binary_op: bool
    :param binary_op: indicate whether the calculator support free operator (operator can operate operands number larger than 2)
    :type expression: str
    :param expression: input expression
    :rtype: int
    :return: evaluated value for the input expression
    """
    return StackInterpreter(binary_op).evaluate(expression)


def evaluate_interpreter(expression: str, free_op: bool) -> int:
    """
    :type free_op: bool
    :param free_op: indicate whether the calculator support free operator (operator can operate operands number larger than 2)
    :type expression: str
    :param expression: input expression
    :rtype: int
    :return: evaluated value for the input expression
    """
    string = MovableStream(expression)
    lexer = Lexer(string)
    tokens = TokenStream(lexer)
    parser = Parser(tokens, free_op)
    pass
