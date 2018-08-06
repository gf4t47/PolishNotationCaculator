from typing import Optional, Tuple


class PeekableStream:
    def __init__(self, text: str):
        self.__text = text
        self.pos = 0

    def __str__(self):
        return self.__text

    @property
    def current_char(self) -> Optional[str]:
        return self._retrieve(self.pos)

    def _retrieve(self, pos: int) -> Optional[str]:
        return self.__text[pos] if 0 <= pos < len(self.__text) else None

    def peek(self, step: int = 1) -> Tuple[bool, str]:
        got = self._retrieve(self.pos + step)
        return (True, got) if got is not None else (False, '')


class MovableStream(PeekableStream):
    def advance(self, step: int = 1):
        self.pos += step
