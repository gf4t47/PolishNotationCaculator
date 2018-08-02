import pytest
from src.calculator import op_calc_map
from src.main import evaluate

left_data = [0, 1, 2, 10, 2]
right_data = [0, 1, 3, 22]


def unary_generator(inputs):
    result = []
    for it in inputs:
        for expr in [f'{it}', f'0{it}', f'({it})', f'(00{it})']:
                result.append((expr, it))
    return result


def binary_generator(llist, rlist, op_key):
    result = []
    for left, right in [(l, r) for l in llist for r in rlist if op_key != '/' or r != 0]:
        calculated = op_calc_map[op_key](left, right)
        for expr in [f'{op_key} {left} {right}', f'{op_key} 00{left} {right}', f'({op_key} {left} {right})', f'({op_key} {left} 0{right})']:
            result.append((expr, calculated))
    return result


@pytest.mark.parametrize("expr, expected", unary_generator(set(left_data + right_data)))
@pytest.mark.parametrize("binary_op", [True, False])
def test_unary(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)


@pytest.mark.parametrize("expr, expected", binary_generator(left_data, right_data, '+'))
@pytest.mark.parametrize("binary_op", [True, False])
def test_binary_add(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)


@pytest.mark.parametrize("expr, expected", binary_generator(left_data, right_data, '-'))
@pytest.mark.parametrize("binary_op", [True, False])
def test_binary_sub(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)


@pytest.mark.parametrize("expr, expected", binary_generator(left_data, right_data, '*'))
@pytest.mark.parametrize("binary_op", [True, False])
def test_binary_mul(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)


@pytest.mark.parametrize("expr, expected", binary_generator(left_data, right_data, '/'))
@pytest.mark.parametrize("binary_op", [True, False])
def test_binary_div(expr, expected, binary_op):
    assert expected == evaluate(expr, binary_op)
