from typing import Tuple, Optional

from src.interpreter.lexer.factory.token_factory import TokenFactory
from src.interpreter.lexer.token import Token, TokenType

brackets = {
    '(': Token(TokenType.BRACKET, True),
    ')': Token(TokenType.BRACKET, False)
}


class BracketFactory(TokenFactory):
    def match(self) -> Tuple[int, Optional[Token]]:
        continued, cur_char = self.query(0)
        return (1, brackets[cur_char]) if continued and cur_char in brackets else (0, None)
