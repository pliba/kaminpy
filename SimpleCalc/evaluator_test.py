from pytest import mark, approx

from evaluator import tokenize, evaluate


@mark.parametrize("source, want", [
    ('3', ['3']),
    ('abs', ['abs']),
    ('(now)', ['(', 'now', ')']),
    ('()', ['(', ')']),
    ('(+ 2   3)', ['(', '+', '2', '3', ')']),
    ('(+ 2 (* 3 5))', ['(', '+', '2', '(', '*', '3', '5', ')', ')']),
])
def test_tokenize(source, want):
    tokens = tokenize(source)
    assert want == tokens


@mark.parametrize("source, want", [
    ('2', 2),
    ('(+ 2 3)', 5),
    ('(+ 1 2 3 4)', 10),
    ('(+ 2 (* 3 5))', 17),
    ('(/ (* (- 100 32) 5) 9)', approx(37.7, .01)),
])
def test_eval(source, want):
    result = evaluate(tokenize(source))
    assert want == result
