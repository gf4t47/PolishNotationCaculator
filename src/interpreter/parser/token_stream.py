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

        self._stream.append(Token(TokenType.EOF, 'EOF'))

    def next_token(self)-> Token:
        token = self._stream[self.__pos]
        self.__pos += 1
        return token
