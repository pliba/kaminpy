from pytest import mark, raises

import operator

from parser import parse, tokenize
from evaluator import evaluate, Operator
from evaluator import InvalidOperator, UnknownOperator
from evaluator import MissingArgument, TooManyArguments
from evaluator import EmptyExpression


@mark.parametrize("source,want", [
    ("2", 2),
    ("-2", -2)
])
def test_evaluate_number_literals(source, want):
    expr = parse(tokenize(source))
    assert want == evaluate(expr)


def test_evaluate_builtin():
    expr = parse(tokenize("+"))
    want = Operator(symbol="+", function=operator.add, arity=2)
    assert want == evaluate(expr)


@mark.parametrize("source,want", [
    ("(+ 1 2)", 3),
    ("(* 3 (+ 4 5))", 27),
    # (100°F − 32) * 5 / 9 = 37°C
    ("(/ (* (- 100 32) 5) 9)", 37),
])
def test_evaluate_s_expressions(source, want):
    expr = parse(tokenize(source))
    assert want == evaluate(expr)


def test_evaluate_not_operator():
    expr = parse(tokenize("(2)"))
    with raises(InvalidOperator):
        evaluate(expr)


def test_evaluate_not_operator_with_argument():
    expr = parse(tokenize("(3 4)"))
    with raises(InvalidOperator):
        evaluate(expr)


def test_evaluate_not_operator_message():
    expr = parse(tokenize("(5 6)"))
    with raises(InvalidOperator) as excinfo:
        evaluate(expr)

    assert "Invalid operator: 5." == str(excinfo.value)


def test_evaluate_missing_arguments():
    expr = parse(tokenize("(* 5)"))
    with raises(MissingArgument) as excinfo:
        evaluate(expr)

    want = "Not enough arguments for operator: '*'."
    assert want == str(excinfo.value)


def test_evaluate_too_many_arguments():
    expr = parse(tokenize("(/ 6 7 8)"))
    with raises(TooManyArguments) as excinfo:
        evaluate(expr)

    want = "Too many arguments for operator: '/'."
    assert want == str(excinfo.value)


def test_evaluate_unknown_operator():
    expr = parse(tokenize("@"))
    with raises(UnknownOperator) as excinfo:
        evaluate(expr)

    want = "Unknown operator: '@'."
    assert want == str(excinfo.value)


def test_evaluate_empty_expression():
    expr = parse(tokenize("()"))
    with raises(EmptyExpression):
        evaluate(expr)
