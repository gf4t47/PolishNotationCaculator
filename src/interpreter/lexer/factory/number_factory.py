from typing import Tuple, Optional

from src.interpreter.lexer.factory.token_factory import TokenFactory
from src.interpreter.lexer.token import Token, TokenType


def is_digit(ch: str)-> bool:
    return ch.isdigit()


class NumberFactory(TokenFactory):
    def _integer(self)-> Tuple[int, Optional[Token]]:
        num_str = ''
        step = 0

        continued, cur_char = self.query(step)

        negative = False
        if continued and cur_char == '-':
            negative = True
            step += 1
            continued, cur_char = self.query(step)

        while continued and is_digit(cur_char):
            num_str += cur_char
            step += 1
            continued, cur_char = self.query(step)

        if negative and step > 1:
            return step, Token(TokenType.NUMBER, int(num_str) * -1)
        elif not negative and step > 0:
            return step, Token(TokenType.NUMBER, int(num_str))
        else:
            return 0, None

    def match(self) -> Tuple[int, Optional[Token]]:
        return self._integer()
