import pytest

from src.interpreter.visitor.environment import VariableEnvironment
from src.main import interpreter_calc


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 2,
        'z': 3,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('= x / 4 2 + x 1', 3),
])
@pytest.mark.parametrize("binary_op", [False])
@pytest.mark.parametrize('calc', [interpreter_calc])
def test_expr_assignment(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnvironment(env))