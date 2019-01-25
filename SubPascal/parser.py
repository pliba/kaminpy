#!/usr/bin/env python3

import collections
from typing import Deque, List, Union

import errors


Atom = Union[str, int]
Expression = Union[Atom, List]


def tokenize(source: str) -> Deque[str]:
    spaced = source.replace('(', ' ( ').replace(')', ' ) ')
    return collections.deque(spaced.split())


def parse_atom(token: str) -> Atom:
    if token[0] == '+':
        return token
    try:
        return int(token)
    except ValueError:
        return token


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
        return parse_atom(head)


if __name__ == '__main__':
    import sys
    print(parse_exp(tokenize(sys.stdin.read())))
