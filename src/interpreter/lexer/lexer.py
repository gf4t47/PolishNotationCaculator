from interpreter.input.string_stream import MovableStream
from interpreter.lexer.factory.bracket_factory import BracketFactory
from interpreter.lexer.factory.number_factory import NumberFactory
from interpreter.lexer.factory.operator_factory import OperatorFactory
from interpreter.lexer.token import Token, TokenType


def is_blank(ch: str)-> bool:
    return ch.isspace()


class Lexer:
    def __init__(self, stream: MovableStream):
        self.stream = stream
        self.bracket_factory = BracketFactory(stream)
        self.number_factory = NumberFactory(stream)
        self.operator_factory = OperatorFactory(stream)

    @property
    def _movable_stream(self)-> MovableStream:
        return self.stream

    @property
    def _continued(self):
        return self._movable_stream.current_char is not None

    def _skip_blank(self):
        while self._continued and is_blank(self._movable_stream.current_char):
            self._movable_stream.advance()

    def next_token(self) -> Token:
        while self._continued:
            num_length, num_token = self.number_factory.match()
            if num_length > 0:
                self._movable_stream.advance(num_length)
                return num_token

            operator_length, operator_token = self.operator_factory.match()
            if operator_length > 0:
                self._movable_stream.advance(operator_length)
                return operator_token

            bracket_length, bracket_token = self.bracket_factory.match()
            if bracket_length > 0:
                self._movable_stream.advance(bracket_length)
                return bracket_token

            if is_blank(self._movable_stream.current_char):
                self._skip_blank()
            else:
                raise SyntaxError(f'unrecognized character {self._movable_stream.current_char}')

        return Token(TokenType.EOF, 'EOF')
