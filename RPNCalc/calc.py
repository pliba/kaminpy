#!/usr/bin/env python3

import sys
import inspect


OPERATORS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
}


def evaluate(tokens, stack):
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


def format_stack(stack):
    if len(stack) == 0:
        return '[]'
    items = [str(n) for n in stack[:-1]] + [f'[{stack[-1]}]']
    return ' '.join(items)


def repl(input_fn=input):
    """Read-Eval-Print-Loop"""
    print(f'To clear stack, type {CLEAR_COMMAND}', file=sys.stderr)
    stack = []
    while True:
        try:
            line = input_fn('> ')   # Read
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line == CLEAR_COMMAND:
            stack = []
        else:
            stack_backup = stack[:]
            try:
                evaluate(line.split(), stack)   # Eval
            except IndexError:
                print('*** Not enough arguments.', file=sys.stderr)
                stack = stack_backup
        print(format_stack(stack))                  # Print


if __name__ == '__main__':
    repl()
