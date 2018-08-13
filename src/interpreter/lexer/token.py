from enum import Enum
from attr import dataclass


class TokenType(Enum):
    EOF = 0
    NUMBER = 1
    CALCULATOR = 2
    BRACKET = 3
    VARIABLE = 4
    ASSIGN = 5

    def __str__(self):
        return str(self.name)


@dataclass
class Token:
    type: TokenType
    value: (int, str, bool)

    def __str__(self):
        return f'TOKEN({self.value}:{self.type})'
