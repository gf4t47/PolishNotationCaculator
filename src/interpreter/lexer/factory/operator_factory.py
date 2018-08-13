from typing import Tuple, Optional

from src.operators import calc_op_map
from src.interpreter.lexer.factory.token_factory import TokenFactory
from src.interpreter.lexer.token import Token, TokenType

operators = {op: Token(TokenType.CALCULATOR, op) for op in calc_op_map}
operators['='] = Token(TokenType.ASSIGN, '=')


class OperatorFactory(TokenFactory):
    def match(self) -> Tuple[int, Optional[Token]]:
        continued, cur_char = self.query(0)
        return (1, operators[cur_char]) if continued and cur_char in operators else (0, None)
