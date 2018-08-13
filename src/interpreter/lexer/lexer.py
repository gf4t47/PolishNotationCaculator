from interpreter.lexer.factory.variable_factory import VariableFactory
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
        self._factories = [
            NumberFactory(stream),
            VariableFactory(stream),
            OperatorFactory(stream),
            BracketFactory(stream),
        ]

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
            if is_blank(self._movable_stream.current_char):
                self._skip_blank()

            for factory in self._factories:
                matched, token = factory.match()
                if matched > 0:
                    self._movable_stream.advance(matched)
                    return token

            raise SyntaxError(f'unrecognized character {self._movable_stream.current_char}')

        return Token(TokenType.EOF, 'EOF')
