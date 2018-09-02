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
    (' + x (= y 1000 (= y 10 + x y)) z y', 11),
    (' = x 5 + x (= y 10 = x (* 10 10) + x y) z y', 114),
])
def test_variable_shadowing(expr, env, expected):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 1,
        'z': 1,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('+ x ( = x (+ x 1) x )', 3),
    (' + '
        'x '
        '( = x (= x (+ x 1) + x 1) '
     '     + x 1 )', 5),
])
def test_variable_sel_assignment(expr, env, expected):
    assert expected == calculate(expr, env)
