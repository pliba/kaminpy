from collections import deque
from typing import TypeAlias


def tokenize(source: str) -> deque[str]:
    spaced = source.replace('(', ' ( ').replace(')', ' ) ')
    return deque(spaced.split())


Number: TypeAlias = int | float
Atom: TypeAlias = str | float
Expression: TypeAlias = Atom | list


def parse_number(s: str) -> Number:
    if '.' in s:
        f = float(s)
        i = int(f)
        return i if i == f else f
    else:
        return int(s)


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
            return parse_number(head)
        except ValueError:
            return head


if __name__ == '__main__':
    import sys
    print(parse(tokenize(sys.stdin.read())))
