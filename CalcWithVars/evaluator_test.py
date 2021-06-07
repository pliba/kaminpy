from math import isclose
from pytest import mark, raises

from evaluator import evaluate, global_env
import errors


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


def test_evaluate_undefined_variable():
    ast = 'x'
    with raises(errors.UndefinedVariable) as excinfo:
        evaluate(ast)
    assert "Undefined variable: 'x'." == str(excinfo.value)


def test_let():
    ast = ['let', 'test_let_var', ['/', 6, 2]]
    want_name = 'test_let_var'
    want_value = 3
    got = evaluate(ast)
    assert want_value == got
    assert want_name in global_env
    assert want_value == global_env[want_name]
    del global_env[want_name]
