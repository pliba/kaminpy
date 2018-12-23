#!/usr/bin/env python3

import sys

from parser import parse_exp, tokenize
from evaluator import evaluate, define_function
from repl import repl
import errors


def run(source_file):
    """Read and execute opened source file"""
    source = source_file.read()

    tokens = tokenize(source)

    while tokens:
        try:
            current_exp = parse_exp(tokens)
        except errors.UnexpectedCloseParen as exc:
            print('***', exc, file=sys.stderr)
            break

        if isinstance(current_exp, list) and current_exp[0] == 'define':
            define_function(current_exp[1:])
        else:
            try:
                evaluate({}, current_exp)
            except errors.EvaluatorException as exc:
                print('***', exc, file=sys.stderr)
                continue


def main(args):
    if not args:
        repl()
    else:
        with open(args[0]) as source_file:
            run(source_file)


if __name__ == '__main__':
    main(sys.argv[1:])
