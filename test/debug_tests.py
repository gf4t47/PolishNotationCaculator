import pytest
from src.main import evaluate


@pytest.mark.parametrize("expr, expected, binary_op", [('(+ 1 (- 0 1))', 0, False)])
def test(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)
