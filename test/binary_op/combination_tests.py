import pytest
from tools.expression_builder import ternary_generator
from src.main import evaluate

left_data = [1]
right_data = [1]


@pytest.mark.parametrize("expr, expected", ternary_generator(left_data, right_data, '+', '+'))
@pytest.mark.parametrize("binary_op", [True, False])
def test_ternary_add_add(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)
