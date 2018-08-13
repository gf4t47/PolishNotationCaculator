import pytest

from src.interpreter.visitor.enviroment import VariableEnviroment
from src.main import interpreter_calc
from src.main import stack_calc


@pytest.mark.parametrize('env', [
    {
        'x': -1,
        'ya': 0,
        'zbc': 1,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('+ 1 1', 2),
    ('+ x 1', 0),
    ('+ ya 1', 1),
    ('+ zbc 1', 2),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [stack_calc, interpreter_calc])
def test_variable(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnviroment(env))


@pytest.mark.parametrize('env', [
    {
        'x': -1,
        'y': 0,
        'z': 1,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('+ 1 1', 2),
    ('+ x 1', 0),
    ('= x 1 + x 1', 2),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [interpreter_calc])
def test_assignment(expr, expected, binary_op, calc, env):
    assert expected == calc(expr, binary_op, VariableEnviroment(env))
