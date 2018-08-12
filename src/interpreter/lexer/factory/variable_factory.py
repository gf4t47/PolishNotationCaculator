from typing import Tuple, Optional

from src.interpreter.lexer.token import Token, TokenType
from src.interpreter.lexer.factory.token_factory import TokenFactory


def is_alpha(ch: str)-> bool:
    return ch.isalpha()


class VariableFactory(TokenFactory):
    def _letter(self)->Tuple[int, Optional[Token]]:
        name = ''
        step = 0

        continued, cur_char = self.query(step)
        while continued and is_alpha(cur_char):
            name += cur_char
            step += 1
            continued, cur_char = self.query(step)

        return (step, Token(TokenType.VARIABLE, name)) if step > 0 else (0, None)

    def match(self) -> Tuple[int, Optional[Token]]:
        return self._letter()
