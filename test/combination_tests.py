import pytest
from tools.expression_builder import ternary_generator_all_op
from src.main import stack_calc as evaluate

left_data = [0, 1, 10]
right_data = [1, 343]


@pytest.mark.parametrize("expr, expected", ternary_generator_all_op(left_data, right_data, None))
def test_ternary_binary_op(expr, expected):
    assert expected == evaluate(expr, True)


@pytest.mark.parametrize("expr, expected", ternary_generator_all_op(left_data, right_data, True))
def test_ternary_free_op(expr, expected):
    assert expected == evaluate(expr, False)
