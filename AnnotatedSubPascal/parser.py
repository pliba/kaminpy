#!/usr/bin/env python3

import collections

import errors

from typing import NewType, Deque, Union, List

Symbol = NewType('Symbol', str)
Number = NewType('Number', int)
Atom = Union[Symbol, Number]
Expression = Union[Atom, List]


def tokenize(source: str) -> Deque[str]:
    spaced = source.replace('(', ' ( ').replace(')', ' ) ')
    return collections.deque(spaced.split())


def parse_token(token: str) -> Union[Symbol, Number]:
    if token[0] == '+':
        return Symbol(token)
    try:
        return Number(int(token))
    except ValueError:
        return Symbol(token)


def parse_exp(tokens: Deque[str]) -> Expression:
    head = tokens.popleft()
    if head == '(':
        ast = []
        while tokens and tokens[0] != ")":
            ast.append(parse_exp(tokens))
        if not tokens:
            raise errors.UnexpectedEndOfSource()
        tokens.popleft()  # discard ')'
        return ast
    elif head == ')':
        raise errors.UnexpectedCloseParen()
    else:
        return parse_token(head)


if __name__ == '__main__':
    import sys
    print(parse_exp(tokenize(sys.stdin.read())))
