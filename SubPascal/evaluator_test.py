from pytest import raises

from evaluator import evaluate
import errors


def test_evaluate_number():
    got = evaluate(7, {})
    assert 7 == got


def test_evaluate_undefined_variable():
    with raises(errors.UndefinedVariable) as excinfo:
        evaluate('x', {})

    assert "Undefined variable: 'x'." == str(excinfo.value)
