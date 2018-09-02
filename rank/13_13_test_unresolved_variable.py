import pytest

from src.index import calculate


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 0,
        'z': -1
    }
])
@pytest.mark.parametrize("expr, expected", [
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
])
def test_simplified_expr_is_determined(expr, env, expected):
    actual = calculate(expr, env)
    assert isinstance(actual, str)
    assert expected == actual


@pytest.mark.parametrize('open_env', [
    {
        'x': 1,
        'y': 0,
        'z': -1
    }
])
@pytest.mark.parametrize('hidden_env', [
    {
        'a': 1,
        'b': 0,
        'c': -1
    }
])
@pytest.mark.parametrize("expr, expected", [
    ('+ x y a 3', 5),
    ('+ (+ x a) (+ y b)', 2),
    ('+ (+ x a) (+ y b) (+ z c)', 0)
])
def test_simplified_expr_is_alterable(expr, open_env, hidden_env, expected):
    number_ret = calculate(expr, {**open_env, **hidden_env})
    assert isinstance(expected, int)
    assert expected == number_ret

    expr_ret = calculate(expr, open_env)
    assert isinstance(expr_ret, str)

    final_ret = calculate(expr_ret, hidden_env)
    assert expected == final_ret
