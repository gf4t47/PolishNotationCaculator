import pytest

from src.interpreter.visitor.enviroment import VariableEnviroment
from src.main import interpreter_calc
from src.main import stack_calc

global_env = VariableEnviroment({
    'x': -1,
    'ya': 0,
    'zbc': 1,
})


@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('+ 1 1', 2),
    ('+ x 1', 0),
    ('+ ya 1', 1),
    ('+ zbc 1', 2),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [stack_calc, interpreter_calc])
def test_free_op(expr, expected, binary_op, calc):
    assert expected == calc(expr, binary_op, global_env)
