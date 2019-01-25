import collections

from typing import Deque

def tokenize(source: str) -> Deque[str]:
    spaced = source.replace('(', ' ( ').replace(')', ' ) ')
    return collections.deque(spaced.split())


def parse_exp(tokens):
    head = tokens.popleft()
    if head == '(':
        ast = []
        while tokens[0] != ")":
            ast.append(parse_exp(tokens))
        tokens.popleft()  # drop ')'
        return ast
    try:
        return int(head)
    except ValueError:
        return head
