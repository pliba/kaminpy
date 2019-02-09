from pytest import mark, raises

from evaluator import evaluate, global_environment
import errors


def test_evaluate_number():
    got = evaluate(7)
    assert 7 == got


@mark.parametrize("ast, value", [
    (['+', 1, 2], 3),
    (['*', 6, ['+', 3, 4]], 42),
    (['/', ['*', ['-', 100, 32], 5], 9], 37)
])
def test_expression(ast, value):
        got = evaluate(ast)
        assert value == got


def test_evaluate_undefined_variable():
    ast = 'x'
    with raises(errors.UndefinedVariable) as excinfo:
        evaluate(ast)
    assert "Undefined variable: 'x'." == str(excinfo.value)


def test_set():
    ast = ['set', 'test_set_var', ['/', 6, 2]]
    want_name = 'test_set_var'
    want_value = 3
    got = evaluate(ast)
    assert want_value == got
    assert want_name in global_environment
    assert want_value == global_environment[want_name]
    del global_environment[want_name]
