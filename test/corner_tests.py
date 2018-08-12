import pytest

from src.main import stack_calc
from src.main import interpreter_calc


@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('( 1 )', 1),
    ('(( 1 ))', 1),
    ('+ 1 1', 2),
    ('( + 1 1 )', 2),
    ('+ 1 1 1', 3),
    ('( + 1 1 1 )', 3),
    ('+ 1 ( + 1 1 1 )', 4),
    ('(((( + 1 ( + 1 1 1 )))))', 4),
    ('(((( + 1 ( + 1 (( + (1) 1 ))) 1))))', 5),
])
@pytest.mark.parametrize("binary_op", [False])
@pytest.mark.parametrize('calc', [stack_calc, interpreter_calc])
def test(expr, expected, binary_op, calc):
    assert expected == calc(expr, binary_op)
