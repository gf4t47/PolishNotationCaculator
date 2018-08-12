import pytest

from src.interpreter.visitor.enviroment import VariableEnviroment
from src.main import interpreter_calc

global_env = VariableEnviroment({
    'x': -1,
    'y': 0,
    'z': 1,
})


@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('+ 1 1', 2),
    ('+ x 1', 0),
    ('+ y 1', 1),
    ('+ z 1', 2),
])
@pytest.mark.parametrize("binary_op", [False, True])
@pytest.mark.parametrize('calc', [interpreter_calc])
def test_free_op(expr, expected, binary_op, calc):
    assert expected == calc(expr, binary_op, global_env)
