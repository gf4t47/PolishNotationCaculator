import pytest

from src.index import calculate


@pytest.mark.parametrize("expr, expected", [
    ('1', 1),
    ('+ 1 1', 2),
    ('- 1 1', 0),
    ('* 1 1', 1),
    ('/ 1 1', 1)
])
def test_basic(expr, expected):
    assert expected == calculate(expr)


@pytest.mark.parametrize("expr, expected", [
    ('/ 1 1', 1),
    ('/ 0 1', 0),
    ('/ 4 2', 2),
    ('/ 3 2', 1),
    ('/ 1 2', 0)
])
def test_integer_division(expr, expected):
    assert expected == calculate(expr)


@pytest.mark.parametrize('env', [
    {
        'x': 1,
    }
])
@pytest.mark.parametrize("expr, expected", [
    ('x', 1),
    ('+ x -1', 0),
])
def test_variable(expr, expected, env):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize('env', [
    {
        'x': 1,
    }
])
@pytest.mark.parametrize("expr, expected", [
    ('= x 0 x', 0),
    ('= x 0 + x x', 0)
])
def test_reassignment(expr, expected, env):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 0,
        'z': -1
    }
])
@pytest.mark.parametrize("expr, expected", [
    (' + x (= y 1000 (= y 10 + x y)) z y', 11),
])
def test_variable_shadowing(expr, expected, env):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 0,
        'z': -1
    }
])
@pytest.mark.parametrize("expr, expected", [
    ('+ x ( = x (+ x 1) x )', 3),
])
def test_self_assignment(expr, expected, env):
    assert expected == calculate(expr, env)
