from src.interpreter.lexer.lexer import Lexer
from src.interpreter.lexer.token import TokenType, Token


class TokenStream:
    def __init__(self, lexer: Lexer):
        self.__pos = 0
        self._stream = []
        cur_token = lexer.next_token()
        while cur_token.type != TokenType.EOF:
            self._stream.append(cur_token)
            cur_token = lexer.next_token()
        self._stream.append(cur_token)

    def next_token(self)-> Token:
        token = self._stream[self.__pos]
        self.__pos += 1
        return token

    def current(self)-> int:
        return self.__pos

    def reset(self, index: int):
        if 0 <= index < len(self._stream):
            self.__pos = index
        raise IndexError(f'index argument must be between 0 and {len(self._stream) - 1}, but input is ${index}')
