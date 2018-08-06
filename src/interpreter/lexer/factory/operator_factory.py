from typing import Tuple, Optional

from src.calculator import op_calc_map
from interpreter.lexer.factory.token_factory import TokenFactory
from interpreter.lexer.token import Token, TokenType

operators = {op: Token(TokenType.OPERATOR, op) for op in op_calc_map}


class OperatorFactory(TokenFactory):
    def match(self) -> Tuple[int, Optional[Token]]:
        continued, cur_char = self.query(0)
        return (1, operators[cur_char]) if continued and cur_char in operators else (0, None)
