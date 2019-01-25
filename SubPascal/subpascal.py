#!/usr/bin/env python3

import sys
from typing import List

from parser import parse_exp, tokenize
from evaluator import evaluate, define_function, ValueEnv
from repl import repl
import errors


def env_from_args(args: List[str]) -> ValueEnv:
    env = {}
    for arg in (a for a in args if ':' in a):
        parts = arg.split(':')
        if len(parts) != 2 or not all(parts):
            continue
        name, val = parts
        try:
            num = int(val)
        except ValueError:
            continue
        env[name] = num
    return env


def run(source_file, env: ValueEnv = None):
    """Read and execute opened source file"""
    source = source_file.read()
    if env is None:
        env = {}
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
                evaluate(env, current_exp)
            except errors.EvaluatorException as exc:
                print('***', exc, file=sys.stderr)
                continue


def main(args):
    if not args:
        repl()
    else:
        env = env_from_args(args[1:])
        with open(args[0]) as source_file:
            run(source_file, env)


if __name__ == '__main__':
    main(sys.argv[1:])
