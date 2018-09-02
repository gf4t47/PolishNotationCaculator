import pytest

from src.index import calculate
from src.main import interpreter_calc


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
def test_simplified_expr_is_alterable(expr, env, expected):
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
@pytest.mark.parametrize("expr", [
    '+ x y a 3',
    '+ (+ x a) (+ y b)'
    '+ (+ x a) (+ y b) (+ z c)'
])
def test_simplified_expr_is_alterable(expr, open_env, hidden_env):
    expected = interpreter_calc(expr, False, {**open_env, **hidden_env})
    simplified = calculate(expr, open_env)
    assert isinstance(simplified, str)
    actual = calculate(simplified, hidden_env)
    assert expected == actual
