from src.interpreter.lexer.token import TokenType, Token
from src.interpreter.parser.token_stream import TokenStream


class Parser:
    def __init__(self, tokens: TokenStream):
        self._token_streams = tokens
        self.current_token = self._token_streams.next_token()

    @property
    def current_token(self)-> Token:
        return self._current_token

    @current_token.setter
    def current_token(self, value: Token):
        self._current_token = value

    def eat(self, token_type: TokenType)-> bool:
        if self.current_token.type == token_type:
            self.current_token = self._token_streams.next_token()
            return True

        raise TypeError(f'unexpected token type {self.current_token.type}, expecting {type}')

    def term(self):
        pass

    def parse(self):
        node = self.term()

        if self.current_token.type != TokenType.EOF:
            raise TypeError(f'the token stream is not finished after parsing, last token = {self.current_token}')

        return node

