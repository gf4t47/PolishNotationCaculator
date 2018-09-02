from typing import Dict
from src.main import interpreter_calc


def calculate(expression: str, env: Dict[str, int] = None)-> int:
    return interpreter_calc(expression, False, env)
