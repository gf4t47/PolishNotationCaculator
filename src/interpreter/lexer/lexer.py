from src.interpreter.input.string_stream import MovableStream
from src.interpreter.lexer.factory.bracket_factory import BracketFactory
from src.interpreter.lexer.factory.number_factory import NumberFactory
from src.interpreter.lexer.factory.operator_factory import OperatorFactory
from src.interpreter.lexer.token import TokenType, Token


def is_blank(ch: str)-> bool:
    return ch.isspace()


class Lexer:
    def __init__(self, stream: MovableStream):
        self.__stream = stream
        self._bracket_factory = BracketFactory(stream)
        self._number_factory = NumberFactory(stream)
        self._operator_factory = OperatorFactory(stream)

    @property
    def _movable_stream(self)-> MovableStream:
        return self.__stream

    @property
    def _continued(self):
        return self._movable_stream.current_char is not None

    def _skip_blank(self):
        while self._continued and is_blank(self._movable_stream.current_char):
            self._movable_stream.advance()

    def next_token(self) -> Token:
        while self._continued:
            num_length, num_token = self._number_factory.match()
            if num_length > 0:
                self._movable_stream.advance(num_length)
                return num_token

            operator_length, operator_token = self._operator_factory.match()
            if operator_length > 0:
                self._movable_stream.advance(operator_length)
                return operator_token

            bracket_length, bracket_token = self._bracket_factory.match()
            if bracket_length > 0:
                self._movable_stream.advance(bracket_length)
                return bracket_token

            if is_blank(self._movable_stream.current_char):
                self._skip_blank()
            else:
                raise SyntaxError(f'unrecognized character {self._movable_stream.current_char}')

        return Token(TokenType.EOF, 'EOF')
