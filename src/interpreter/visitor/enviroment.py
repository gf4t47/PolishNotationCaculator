from typing import Dict, Optional
import copy


class VariableEnviroment:
    def __init__(self, v_map: Dict[str, int]=None, prev: 'VariableEnviroment'=None):
        self._map = copy.deepcopy(v_map) if v_map is not None else {}
        self._previous = prev

    @property
    def v_map(self) -> Dict[str, int]:
        return self._map

    @property
    def previous(self)->Optional['VariableEnviroment']:
        return self._previous

    def define(self, name: str, val: int) -> None:
        self.v_map[name] = val

    def lookup(self, name: str) -> int:
        if name in self.v_map:
            return self.v_map[name]

        if self.previous is not None:
            return self.previous.lookup(name)

        raise KeyError(f"Can't resolve variable {name}")

