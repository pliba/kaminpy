#!/usr/bin/env python
# coding: utf-8

from pytest import raises

from listep import *

def test_tokenize_atom():
    assert tokenize('3') == ['3']

def test_tokenize_call():
    assert tokenize('(+ 2 3)') == ['(','+','2','3',')']

def test_tokenize_call_with_call():
    assert tokenize('(+ 2 (* 3 4))') == ['(','+','2','(','*','3','4',')',')']

def test_parse_number():
    assert parse('3') == 3

def test_parse_numexp():
    assert parse('(+ 2 3)') == ['+', 2, 3]

def test_parse_numexp_inner():
    assert parse('(+ 2 (* 3 4))') == ['+', 2, ['*', 3, 4]]

def test_parse_empty_paren():
    assert parse('()') == []

def test_parse_empty():
	with raises(UnexpectedEndOfInput):
		parse('')

def test_parse_right_paren():
	with raises(UnexpectedRightParen):
		parse(')')

def test_parse_open_paren():
    with raises(UnexpectedEndOfInput):
        parse('(')

def test_parse_right_paren_detail():
    try:
        parse(')')
    except UnexpectedRightParen as exc:
        assert str(exc) == 'unexpected )'

def test_parse_plus_one():
    assert parse('(++ 2)') == ['++', 2]

def test_eval_int():
    assert evaluate(parse('3')) == 3

def test_eval_op():
    import operator
    assert evaluate(parse('+')) == operator.add

def test_eval_numexp():
    assert evaluate(parse('(+ 2 3)')) == 5

def test_eval_numexp_inner():
    assert evaluate(parse('(+ 2 (* 3 4))')) == 14

def test_eval_no_operator():
    with raises(InvalidOperator):
        evaluate(parse('(2)'))

def test_eval_no_operator2():
    with raises(InvalidOperator):
        evaluate(parse('(2 3)'))

def test_eval_no_operator_detail():
    try:
        evaluate(parse('(2 3)'))
    except InvalidOperator as exc:
        assert str(exc) == "invalid operator: 2"

def test_eval_sub():
    assert evaluate(parse('(- 2 3)')) == -1

def test_eval_div():
    assert evaluate(parse('(/ 6 2)')) == 3

def test_eval_div_returns_int():
    assert evaluate(parse('(/ 6 4)')) == 1

def test_eval_div_by_zero():
    with raises(ZeroDivisionError):
        evaluate(parse('(/ 6 0)'))

def test_eval_pow():
    assert evaluate(parse('(** 2 10)')) == 1024

def test_eval_abs():
    assert evaluate(parse('(abs -2)')) == 2

def test_eval_plus_one():
    assert evaluate(parse('(++ 2)')) == 3
