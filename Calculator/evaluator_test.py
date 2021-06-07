from math import isclose
from pytest import mark

from evaluator import evaluate


def test_evaluate_number():
    got = evaluate(7)
    assert 7 == got


@mark.parametrize("ast, expected", [
    (['+', 1, 2], 3),
    (['*', 6, ['+', 3, 4]], 42),
    (['/', 6.0, 3.0], 2),
    (['/', 5, 2], 2.5),
    (['/', ['*', ['-', 100, 32], 5], 9], 37.778)
])
def test_expression(ast, expected):
        got = evaluate(ast)
        assert type(got) is type(expected)
        if isinstance(expected, int):
            assert expected == got
        else:
            assert isclose(expected, got, rel_tol=.01)
