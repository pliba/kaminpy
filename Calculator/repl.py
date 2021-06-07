#!/usr/bin/env python3

import sys

from parser import parse, tokenize
from evaluator import evaluate

QUIT_COMMAND = '.q'


def repl(input_fn=input):
    """Read-Eval-Print-Loop"""
    print(f'To exit, type {QUIT_COMMAND}', file=sys.stderr)

    while True:
        # ___________________________________________ Read
        try:
            line = input_fn('> ')
        except EOFError:
            break
        if line == QUIT_COMMAND:
            break
        if not line:
            continue

        # ___________________________________________ Eval
        current_exp = parse(tokenize(line))
        value = evaluate(current_exp)

        # ___________________________________________ Print
        print(value)


if __name__ == '__main__':
    repl()
