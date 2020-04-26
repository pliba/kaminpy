#!/usr/bin/env python3

import sys
from array import array
from typing import MutableSequence, Callable, List, Iterable, Iterator


OPERATORS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '^': lambda a, b: a ** b,
}


def evaluate(tokens: Iterable[str], stack: MutableSequence[float]) -> None:
    for head in tokens:
        try:
            stack.append(float(head))
        except ValueError:
            op = OPERATORS[head]
            x, y = stack.pop(), stack.pop()
            result = op(y, x)
            stack.append(result)


def format_stack(stack: MutableSequence[float]) -> str:
    items = (repr(n) for n in stack)
    return (' │ '.join(items) + ' →')


def repl(input_fn: Callable[[str], str] = input) -> None:
    """Read-Eval-Print-Loop"""

    print('Use CTRL+C to quit.', file=sys.stderr)
    stack: MutableSequence[float] = array('d')

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
        print(format_stack(stack))             # Print

    print()

if __name__ == '__main__':
    repl()
