import pytest

from src.index import calculate


@pytest.mark.parametrize("env", [{
    'x': -1,
    'y': 1,
    'z': 0
}])
@pytest.mark.parametrize("expr, expected", [
    ('x', -1),
    ('y', 1),
    ('z', 0),
    ('= x 0 x', 0),
    ('= y 0 y', 0),
    ('= z 0 z', 0),
    ('= x 0 + x 1', 1),
    ('= y 0 + y 1', 1),
    ('= z 0 + z 1', 1),
])
def test_assign_with_integer(expr, env, expected):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize("env", [{
    'x': -1,
    'y': 1,
    'z': 0
}])
@pytest.mark.parametrize("expr, expected", [
    ('x', -1),
    ('y', 1),
    ('z', 0),
    ('= x 0 + 1 (+ (* x 0) 1) 1', 3),
    ('= y 0 + 1 (+ 1 (/ y 10)) 1', 3),
    ('= z 0 + 1 (- z 2) 1', 0),
])
def test_assignment_is_global(expr, env, expected):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize("env", [{
    'x': -1,
    'y': 1,
    'z': 0,
    'a': 10,
    'b': -10,
    'c': 0
}])
@pytest.mark.parametrize("expr, expected", [
    ('x', -1),
    ('y', 1),
    ('z', 0),
    ('= x a x', 10),
    ('= y b y', -10),
    ('= z c z', 0),
    ('= x a + x a', 20),
    ('= y b + y b', -20),
    ('= z c + z c', 0),
])
def test_assign_with_variable(expr, env, expected):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize("env", [{
    'x': -1,
    'y': 1,
    'z': 0
}])
@pytest.mark.parametrize("expr, expected", [
    ('x', -1),
    ('y', 1),
    ('z', 0),
    ('= x (+ 1 1) x', 2),
    ('= y (- 1 1) y', 0),
    ('= z (* 1 1) z', 1),
    ('= x (+ 1 1) + x 1', 3),
    ('= y (- 1 1) + y 1', 1),
    ('= z (* 1 1) + z 1', 2),
])
def test_assign_with_integer_expression(expr, env, expected):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize('env', [
    {
        'x': 1,
        'y': 2,
        'z': 3,
    },
])
@pytest.mark.parametrize("expr, expected", [
    ('= y 10 = x (+ 1 y) (+ x 1)', 12),
    ('= x (/ 4 z) + x 1', 2),
])
def test_assign_with_variable_expression(expr, env, expected):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize("expr, expected", [
    ('= x 1 x', 1),
    ('= y 2 y', 2),
    ('= z 3 z', 3),
    ('= x 1 = y 2 = z 3 + x y z', 6),
])
def test_no_env_assignment_cover_every_variable(expr, expected):
    assert expected == calculate(expr)
