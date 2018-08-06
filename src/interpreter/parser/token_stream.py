from src.interpreter.lexer.lexer import Lexer
from src.interpreter.lexer.token import TokenType, Token


class TokenStream:
    def __init__(self, lexer: Lexer):
        self.pos = 0
        self.stream = []
        cur_token = lexer.next_token()
        while cur_token.type != TokenType.EOF:
            self.stream.append(cur_token)
            cur_token = lexer.next_token()

        self.stream.append(Token(TokenType.EOF, 'EOF'))

    def next_token(self)-> Token:
        token = self.stream[self.pos]
        self.pos += 1
        return token
