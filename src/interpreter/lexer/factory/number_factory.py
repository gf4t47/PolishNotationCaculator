from typing import Tuple, Optional

from interpreter.lexer.factory.token_factory import TokenFactory
from interpreter.lexer.token import Token, TokenType


def is_digit(ch: str)-> bool:
    return ch.isdigit()


class NumberFactory(TokenFactory):
    def integer(self)-> Tuple[int, Optional[Token]]:
        result = ''
        step = 0

        continued, cur_char = self.query(step)
        while continued and is_digit(cur_char):
            result += cur_char
            step += 1
            continued, cur_char = self.query(step)

        return (step, Token(TokenType.NUMBER, int(result))) if step > 0 else (0, None)

    def match(self) -> Tuple[int, Optional[Token]]:
        return self.integer()
