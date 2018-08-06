import functools
import logging
import sys

from attr import dataclass
from src.calculator import op_calc_map

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


@dataclass
class NumberToken:
    value: int


NumberToken.terminal = NumberToken(-1)


class StackInterpreter:
    def __init__(self: object, binary_op: bool) -> None:
        self.__number_stack = []
        self._binary_op = binary_op

    @property
    def _number_stack(self):
        return self.__number_stack

    def _binary_op_calc(self, char):
        left = self._number_stack.pop()
        right = self._number_stack.pop()
        # logging.debug(f'{char} {left.value} {right.value}')
        return op_calc_map[char](left.value, right.value)

    def _free_op_calc(self, char):
        operands = []

        while len(self._number_stack) > 0:
            cur_token = self._number_stack.pop()
            if cur_token is not NumberToken.terminal:
                operands.append(cur_token.value)
            else:
                break

        # logging.debug(f'{char} {operands}')
        return functools.reduce(op_calc_map[char], operands)

    def _calc(self, char):
        capability = len(self._number_stack)
        if capability < 2:
            raise BufferError(f'Not enough operands, length = {capability}')
        return self._binary_op_calc(char) if self._binary_op else self._free_op_calc(char)

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
                ret = self._calc(cur)
                self._number_stack.append(NumberToken(ret))
                index -= 1
            elif cur.isdigit():
                num_str = ''
                while index >= 0 and cur.isdigit():
                    num_str += cur
                    index -= 1
                    cur = expression[index]
                self._number_stack.append(NumberToken(int(num_str[::-1])))
            elif cur == ')':
                if not self._binary_op:
                    self._number_stack.append(NumberToken.terminal)
                index -= 1
            else:
                raise SyntaxError(f'unrecognized character: {cur}')

        return self._number_stack.pop().value
