#!/usr/bin/env python3

import collections
from typing import Deque, List, Union


Atom = Union[str, int]
Expression = Union[Atom, List]


def tokenize(source: str) -> Deque[str]:
    spaced = source.replace('(', ' ( ').replace(')', ' ) ')
    return collections.deque(spaced.split())


def parse(tokens: Deque[str]) -> Expression:
    head = tokens.popleft()
    if head == '(':
        ast = []
        while tokens[0] != ")":
            ast.append(parse(tokens))
        tokens.popleft()  # discard ')'
        return ast
    try:
        return int(head)
    except ValueError:
        return head


if __name__ == '__main__':
    import sys
    print(parse(tokenize(sys.stdin.read())))
