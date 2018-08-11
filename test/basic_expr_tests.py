import pytest
from tools.expression_builder import unary_generator, binary_generator
from src.main import evaluate_stack as evaluate


left_data = [0, 1, 2, 10, 2]
right_data = [0, 1, 3, 22]


@pytest.mark.parametrize("expr, expected", unary_generator(set(left_data + right_data)))
@pytest.mark.parametrize("binary_op", [True, False])
def test_unary(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)


@pytest.mark.parametrize("expr, expected", binary_generator(left_data, right_data, '+', None))
@pytest.mark.parametrize("binary_op", [True, False])
def test_binary_add(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)


@pytest.mark.parametrize("expr, expected", binary_generator(left_data, right_data, '-', None))
@pytest.mark.parametrize("binary_op", [True, False])
def test_binary_sub(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)


@pytest.mark.parametrize("expr, expected", binary_generator(left_data, right_data, '*', None))
@pytest.mark.parametrize("binary_op", [True, False])
def test_binary_mul(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)


@pytest.mark.parametrize("expr, expected", binary_generator(left_data, right_data, '/', None))
@pytest.mark.parametrize("binary_op", [True, False])
def test_binary_div(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)
