from typing import Dict


class VariableEnviroment:
    def __init__(self, v_map:Dict[str, int]=None):
        self._map = v_map if v_map is not None else {}

    @property
    def v_map(self) -> Dict[str, int]:
        return self._map

    def define(self, name: str, val: int) -> None:
        self.v_map[name] = val

    def lookup(self, name: str) -> int:
        return self.v_map[name]
