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
    else:
        try:
            return float(head) if '.' in head else int(head)
        except ValueError:
            return head


if __name__ == '__main__':
    import sys
    print(parse(tokenize(sys.stdin.read())))
