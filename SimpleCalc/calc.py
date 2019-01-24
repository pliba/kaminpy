#!/usr/bin/env python3

import sys

from typing import List, Dict, Callable

def tokenize(source: str) -> List[str]:
    spaced = source.replace('(', ' ( ').replace(')', ' ) ')
    return spaced.split()


OPERATORS: Dict[str, Callable[[float, float], float]] = {
    '+': lambda *args: sum(args),
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
}


def evaluate(tokens: List[str]) -> float:
    head = tokens.pop(0)
    if head == '(':
        op = OPERATORS[tokens.pop(0)]
        args = []
        while tokens[0] != ')':
            args.append(evaluate(tokens))
        tokens.pop(0)  # drop ')'
        return op(*args)
    else:
        return float(head)


QUIT_COMMAND = '.q'


def repl(input_fn=input):
    """Read-Eval-Print-Loop"""
    print(f'To exit, type {QUIT_COMMAND}', file=sys.stderr)
    while True:
        line = input_fn('> ')              # Read
        if line == QUIT_COMMAND:
            break
        value = evaluate(tokenize(line))   # Eval
        print(value)                       # Print


if __name__ == '__main__':
    repl()
