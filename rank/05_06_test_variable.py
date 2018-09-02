import pytest

from src.index import calculate


@pytest.mark.parametrize("env", [{
    'x': -1,
    'y': 1,
    'z': 0
}])
@pytest.mark.parametrize("expr, expected", [
    ('x', -1),
    ('(y)', 1),
    ('(((y)))', 1),
    ('+ x ((y))', 0),
    ('(/ z 100)', 0),
    ('(/ (y) (100))', 0)
])
def test_single_character_variable(expr, env, expected):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize("env", [{
    'IamALongVariable': -1
}])
@pytest.mark.parametrize("expr, expected", [
    ('IamALongVariable', -1),
    ('(((IamALongVariable)))', -1),
    ('+ (((IamALongVariable))) 1', 0),

])
def test_multiple_characters_variable(expr, env, expected):
    assert expected == calculate(expr, env)


@pytest.mark.parametrize("env", [{
    'x': -1,
    'X': 1,
    'y': -2,
    'Y': 2,
    'z': -3,
    'Z': 3
}])
@pytest.mark.parametrize("expr, expected", [
    ('x', -1),
    ('X', 1),
    ('y', -2),
    ('Y', 2),
    ('z', -3),
    ('Z', 3),
    ('+ x y z', -6),
    ('+ X Y Z', 6),
    ('+ x X y Y z Z', 0)
])
def test_variable_is_case_sensitive(expr, env, expected):
    assert expected == calculate(expr, env)
