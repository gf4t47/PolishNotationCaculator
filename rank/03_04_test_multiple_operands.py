import pytest

from tools.expression_builder import unary_generator, binary_generator_all_op, multiple_generator_all_op
from index import calculate


left_data = [-1, 0, 1]
right_data = [2, -10]


@pytest.mark.parametrize("expr, expected", [(f"((({raw})))", result) for raw, result in unary_generator(list(set(left_data + right_data)), None)])
def test_unary_with_redundant_brackets(expr, expected):
    assert expected == calculate(expr)


@pytest.mark.parametrize("expr, expected", [(f"((({raw_expr})))", result) for raw_expr, result in binary_generator_all_op(left_data, right_data, None)])
def test_binary_with_redundant_brackets(expr, expected):
    assert expected == calculate(expr)


@pytest.mark.parametrize("expr, expected", [(f'((( + {expr} 1)))', 1 + calculated)
                                            for expr, calculated in
                                            [(f"((({raw_expr})))", result) for raw_expr, result in binary_generator_all_op(left_data, right_data, None)]])
def test_ternary_with_redundant_brackets(expr, expected):
    assert expected == calculate(expr)


@pytest.mark.parametrize("expr, expected", multiple_generator_all_op(list(set(left_data + right_data)), None))
def test_multiple_operands(expr, expected):
    assert expected == calculate(expr)


@pytest.mark.parametrize("expr, expected", [(f'((({expr})))', ret) for expr, ret in multiple_generator_all_op(list(set(left_data + right_data)), None)])
def test_multiple_operands(expr, expected):
    assert expected == calculate(expr)


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
    ('+ 1 ( + 1 1 1 ) 1 1', 6),
    ('+ 1 ( + 1 1 1 ) (- 1 1) 1 1', 6),
    ('(((( + 1 ( + 1 (( + (1) 1 ))) 1))))', 5),
])
def test_multiple_operands_with_bracket(expr, expected):
    assert expected == calculate(expr)


@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('( 1 )', 1),
    ('(( 1 ))', 1),
    ('+ 1 1', 2),
    ('( + 1 1 )', 2),
    ('+ (+ 1 1) 1', 3),
    ('+ 1 (+ 1 1)', 3),
    ('(+ (+ 1 1) (+ 1 1) )', 4),
    ('(+ (((+ 1 1))) (+ (1) 1) )', 4),
    ('(+ (+ (+ 1 1) (+ 1 1) ) (+ 1 1))', 6),
])
def test_binary_operands_with_bracket(expr, expected):
    assert expected == calculate(expr)
