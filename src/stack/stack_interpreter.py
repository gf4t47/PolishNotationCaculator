import functools
from attr import dataclass
from src.calculator import op_calc_map


@dataclass
class NumberToken:
    value: int


NumberToken.terminal = NumberToken(-1)


class StackInterpreter:
    def __init__(self: object, binary_op: bool) -> None:
        self.number_stack = []
        self.binary_op = binary_op

    def binary_op_calc(self, char):
        left = self.number_stack.pop()
        right = self.number_stack.pop()
        return op_calc_map[char](left.value, right.value)

    def free_op_calc(self, char):
        operands = []

        while len(self.number_stack) > 0:
            cur_token = self.number_stack.pop()
            if cur_token != NumberToken.terminal:
                operands.append(cur_token.value)
            else:
                break

        return functools.reduce(op_calc_map[char], operands)

    def calc(self, char):
        capability = len(self.number_stack)
        if capability < 2:
            raise BufferError(f'Not enough operands, length = {capability}')
        return self.binary_op_calc(char) if self.binary_op else self.free_op_calc(char)

    def evaluate(self, expression: str) -> int:
        """
        :type expression: str
        :param expression: input expression
        :rtype: int
        :return:
        """
        index = len(expression) - 1
        while index >= 0:
            cur = expression[index]
            if cur.isspace() or cur == '(':  # ignore character
                index -= 1
            elif cur in op_calc_map:
                ret = self.calc(cur)
                self.number_stack.append(NumberToken(ret))
                index -= 1
            elif cur.isdigit():
                num_str = ''
                while index >= 0 and cur.isdigit():
                    num_str += cur
                    index -= 1
                    cur = expression[index]
                self.number_stack.append(NumberToken(int(num_str[::-1])))
            elif cur == ')':
                self.number_stack.append(NumberToken.terminal)
                index -= 1
            else:
                raise SyntaxError(f'unrecognized character: {cur}')

        return self.number_stack.pop().value
