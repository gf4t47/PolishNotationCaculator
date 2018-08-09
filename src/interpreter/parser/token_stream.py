from src.interpreter.lexer.lexer import Lexer
from src.interpreter.lexer.token import TokenType, Token


class TokenStream:
    def __init__(self, lexer: Lexer):
        self.__pos = 0
        self._peek_pos = 0
        self._stream = []
        cur_token = lexer.next_token()
        while cur_token.type != TokenType.EOF:
            self._stream.append(cur_token)
            cur_token = lexer.next_token()

        self._stream.append(Token(TokenType.EOF, 'EOF'))

    def next_token(self)-> Token:
        token = self._stream[self.__pos]
        self.__pos += 1
        self.reset_peek()
        return token

    def peek_token(self) -> Token:
        token = self._stream[self._peek_pos]
        self._peek_pos += 1
        return token

    def commit_peek(self):
        self.__pos = self._peek_pos

    def reset_peek(self):
        self._peek_pos = self.__pos
