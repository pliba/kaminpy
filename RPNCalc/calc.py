#!/usr/bin/env python3

import sys
from array import array
from typing import MutableSequence, Callable, List, Iterable, Iterator, Sequence


OPERATORS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '^': lambda a, b: a ** b,
}

Stack = MutableSequence[float]


def evaluate(tokens: Iterable[str], stack: Stack) -> None:
    for token in tokens:
        try:
            stack.append(float(token))
        except ValueError:
            op = OPERATORS[token]
            x, y = stack.pop(), stack.pop()
            result = op(y, x)
            stack.append(result)


def display(s: Sequence) -> str:
    items = (repr(n) for n in s)
    return ' │ '.join(items) + ' →'


def repl(input_fn: Callable[[str], str] = input) -> None:
    """Read-Eval-Print-Loop"""

    print('Use CTRL+C to quit.', file=sys.stderr)
    stack: Stack = array('d')

    while True:
        try:
            line = input_fn('> ')              # Read
        except (EOFError, KeyboardInterrupt):
            break
        stack_backup = stack[:]
        try:
            evaluate(line.split(), stack)      # Eval
        except IndexError:
            print('*** Not enough arguments.', file=sys.stderr)
            stack = stack_backup
        except KeyError as exc:
            print('*** Unknown operator:', repr(exc.args[0]), file=sys.stderr)
            stack = stack_backup
        print(display(stack))             # Print

    print()


if __name__ == '__main__':
    repl()
