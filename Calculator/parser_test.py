from pytest import mark

from parser import parse, tokenize


@mark.parametrize("source, ast", [
    ('7', 7),
    ('7.0', 7),
    ('7.7', 7.7),
    ('+', '+'),
])
def test_parse_atoms(source, ast):
    got = parse(tokenize(source))
    assert type(ast) == type(got)
    assert ast == got


@mark.parametrize("source, want", [
    ('a', ['a']),
    ('abs', ['abs']),
    ('(now)', ['(', 'now', ')']),
    ('()', ['(', ')']),
    ('(+ 2   3)', ['(', '+', '2', '3', ')']),
    ('(+ 2 (* 3 5))', ['(', '+', '2', '(', '*', '3', '5', ')', ')']),
])
def test_tokenize(source, want):
    tokens = tokenize(source)
    assert want == list(tokens)


@mark.parametrize("source, ast", [
    ('(+ 1 2)', ['+', 1, 2]),
    ('(if a b c)', ['if', 'a', 'b', 'c']),
    ('(+ 2 (* 3 5))', ['+', 2, ['*', 3, 5]]),
    ('(/ (* (- 100 32) 5) 9)', ['/', ['*', ['-', 100, 32], 5], 9])
])
def test_parse_application(source, ast):
    got = parse(tokenize(source))
    assert ast == got
