from pytest import mark, raises

from parser import parse_exp, tokenize, parse_token

import errors


@mark.parametrize("source, ast", [
    ('7', 7),
    ('+', '+'),
])
def test_parse_exp_atoms(source, ast):
    got = parse_exp(tokenize(source))
    assert ast == got


@mark.parametrize("source, want", [
    ('a', ['a']),
    ('abs', ['abs']),
    ('(now)', ['(', 'now', ')']),
    ('()', ['(', ')']),
    ('(+ 2   3)', ['(', '+', '2', '3', ')']),
    ('(+1  b)', ['(', '+1', 'b', ')']),
    ('(+ 2 (* 3 5))', ['(', '+', '2', '(', '*', '3', '5', ')', ')']),
])
def test_tokenize(source, want):
    tokens = tokenize(source)
    assert want == list(tokens)


@mark.parametrize("source, ast", [
    ('(+ 1 2)', ['+', 1, 2]),
    ('(if a b c)', ['if', 'a', 'b', 'c']),
    ('(+ 2 (* 3 5))', ['+', 2, ['*', 3, 5]]),
    ('(+1  b)', ['+1', 'b']),
    ('(/ (* (- 100 32) 5) 9)', ['/', ['*', ['-', 100, 32], 5], 9])
])
def test_parse_exp_application(source, ast):
    got = parse_exp(tokenize(source))
    assert ast == got


@mark.parametrize("token, ast", [
    ('1', 1),
    ('-1', -1),
    ('abc', 'abc'),
    ('abc-de!', 'abc-de!'),
    ('+', '+'),
    ('+1', '+1'),
])
def test_parse_token(token, ast):
    got = parse_token(token)
    assert ast == got

# _____________________________________________________ Error cases


def test_parse_unexpected_close_parenthesis():
    tokens = tokenize(')')
    with raises(errors.UnexpectedCloseParen) as excinfo:
        parse_exp(tokens)
    assert "Unexpected close parenthesis." == str(excinfo.value)


def test_parse_unexpected_end_of_source():
    tokens = tokenize('(')
    with raises(errors.UnexpectedEndOfSource) as excinfo:
        parse_exp(tokens)
    assert "Unexpected end of source code." == str(excinfo.value)
