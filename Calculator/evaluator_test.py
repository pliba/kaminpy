from pytest import mark

from evaluator import evaluate


def test_evaluate_number():
    got = evaluate(7, {})
    assert 7 == got


@mark.parametrize("ast, value", [
    (['+', 1, 2], 3),
    (['*', 6, ['+', 3, 4]], 42),
    (['/', ['*', ['-', 100, 32], 5], 9], 37)
])
def test_expression(ast, value):
        got = evaluate(ast, {})
        assert value == got
