from typing import Dict, Optional
import copy


class VariableEnvironment:
    def __init__(self, dictionary: Dict[str, int]=None, prev: 'VariableEnvironment'=None):
        self._dict = copy.deepcopy(dictionary) if dictionary is not None else {}
        self._previous = prev

    @property
    def dictionary(self) -> Dict[str, int]:
        return self._dict

    @property
    def previous(self)->Optional['VariableEnvironment']:
        return self._previous

    def define(self, name: str, val: int) -> None:
        self.dictionary[name] = val

    def lookup(self, name: str) -> Optional[int]:
        if name in self.dictionary:
            return self.dictionary[name]

        if self.previous is not None:
            return self.previous.lookup(name)

        # raise KeyError(f"Can't resolve variable {name}")
        return None

