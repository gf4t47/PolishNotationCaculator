import pytest

from index import calculate
from tools.expression_builder import unary_generator, ternary_generator_all_op, binary_generator_all_op

left_data = [-1, 0, 1, 2, 10]
right_data = [-10, 0, 1, 3, 22]


@pytest.mark.parametrize("expr, expected", unary_generator(list(set(left_data + right_data)), None))
def test_unary(expr, expected):
    assert expected == calculate(expr)


@pytest.mark.parametrize("expr, expected", binary_generator_all_op(left_data, right_data, None))
def test_binary_all_op(expr, expected):
    assert expected == calculate(expr)


@pytest.mark.parametrize("expr, expected", ternary_generator_all_op(left_data, right_data, True))
def test_ternary_all_op(expr, expected):
    assert expected == calculate(expr)
