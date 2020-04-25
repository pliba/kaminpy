#!/usr/bin/env python3

import sys
from typing import MutableSequence, Callable, List


OPERATORS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
}


def evaluate(tokens: MutableSequence[str], stack: MutableSequence[float]) -> float:
    while tokens:
        head = tokens.pop(0)
        try:
            stack.append(float(head))
        except ValueError:
            op = OPERATORS[head]
            x, y = stack.pop(), stack.pop()
            result = op(y, x)
            stack.append(result)
    return stack[-1]


CLEAR_COMMAND = 'c'
QUIT_COMMAND = 'q'


def format_stack(stack: MutableSequence[float]) -> str:
    items = (f'{n:.1f}' for n in stack)
    return (' │ '.join(items) + ' →')


def repl(input_fn: Callable[[str], str] = input) -> None:
    """Read-Eval-Print-Loop"""
    print(f'To clear stack, type {CLEAR_COMMAND}', file=sys.stderr)
    print(f'To quit, type {QUIT_COMMAND}', file=sys.stderr)
    stack: List[float] = []
    while True:
        try:
            line = input_fn('> ')                # Read
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line == CLEAR_COMMAND:
            stack = []
        elif line == QUIT_COMMAND:
            return
        else:
            stack_backup = stack[:]
            try:
                evaluate(line.split(), stack)     # Eval
            except IndexError:
                print('*** Not enough arguments.', file=sys.stderr)
                stack = stack_backup
        print(format_stack(stack))                # Print


if __name__ == '__main__':
    repl()
