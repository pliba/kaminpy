from pytest import mark

from parser import parse_exp


@mark.parametrize("line, ast", [
    ('7', 7),
    ('x', 'x'),
])
def test_parse_exp_atoms(line, ast):
    got = parse_exp(line)
    assert ast == got

