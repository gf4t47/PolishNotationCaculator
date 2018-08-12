import pytest
from tools.expression_builder import ternary_generator_all_op
from src.main import stack_calc
from src.main import interpreter_calc

left_data = [0, 1, 10]
right_data = [1, 343]


@pytest.mark.parametrize("expr, expected", ternary_generator_all_op(left_data, right_data, None))
@pytest.mark.parametrize("calc", [stack_calc, interpreter_calc])
def test_ternary_binary_op(expr, expected, calc):
    assert expected == calc(expr, True)


@pytest.mark.parametrize("expr, expected", ternary_generator_all_op(left_data, right_data, True))
@pytest.mark.parametrize("calc", [stack_calc, interpreter_calc])
def test_ternary_free_op(expr, expected, calc):
    assert expected == calc(expr, False)
