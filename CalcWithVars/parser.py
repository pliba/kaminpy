from collections import deque
from typing import Union


def tokenize(source: str) -> deque[str]:
    spaced = source.replace('(', ' ( ').replace(')', ' ) ')
    return deque(spaced.split())


Atom = Union[str, float]
Expression = Union[Atom, list]


def parse(tokens: deque[str]) -> Expression:
    head = tokens.popleft()
    if head == '(':
        ast = []
        while tokens[0] != ")":
            ast.append(parse(tokens))
        tokens.popleft()  # discard ')'
        return ast
    try:
        return float(head)
    except ValueError:
        return head


if __name__ == '__main__':
    import sys
    print(parse(tokenize(sys.stdin.read())))
