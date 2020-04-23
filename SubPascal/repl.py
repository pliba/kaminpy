#!/usr/bin/env python3

import sys

from parser import parse_exp, tokenize, Expression
from evaluator import evaluate, define_function
import errors

from typing import Callable, List, Tuple, NoReturn, cast

QUIT_COMMAND = '.q'


class QuitRequest(Exception):
    """Signal to quit multi-line input."""


def raise_unexpected_paren(line: str) -> NoReturn:
    max_msg_len = 16
    if len(line) < max_msg_len:
        msg = line
    else:
        msg = '\N{HORIZONTAL ELLIPSIS}' + line[-(max_msg_len-1):]
    raise errors.UnexpectedCloseParen(msg)


InputFnType = Callable[[str], str]

def multiline_input(prompt1: str = '',
                    prompt2: str= '',
                    *, 
                    quit_cmd: str = '',
                    input_fn: InputFnType = input) -> str:

    paren_cnt = 0
    lines = []
    prompt = prompt1
    while True:
        line = input_fn(prompt).rstrip()
        if line == quit_cmd:
            raise QuitRequest()
        for char in line:
            if char == '(':
                paren_cnt += 1
            elif char == ')':
                paren_cnt -= 1
            if paren_cnt < 0:
                raise_unexpected_paren(line)
        lines.append(line)
        prompt = prompt2
        if paren_cnt == 0:
            break

    return '\n'.join(lines)


def repl(input_fn: InputFnType = input) -> None:
    """Read-Eval-Print-Loop"""
    print(f'To exit, type {QUIT_COMMAND}', file=sys.stderr)

    while True:
        # ___________________________________________ Read
        try:
            source = multiline_input('> ', '... ',
                                     quit_cmd=QUIT_COMMAND,
                                     input_fn=input_fn)
        except (EOFError, QuitRequest):
            break
        except errors.UnexpectedCloseParen as exc:
            print('***', exc)
            continue
        if not source:
            continue

        # def define_function(parts: Tuple[str, List[str], Expression]) -> str:

        # ___________________________________________ Eval
        current_exp = parse_exp(tokenize(source))
        if isinstance(current_exp, list) and current_exp[0] == 'define':
            result = define_function(*current_exp[1:])
        else:
            try:
                result = str(evaluate({}, current_exp))
            except errors.EvaluatorException as exc:
                print('***', exc)
                continue

        # ___________________________________________ Print
        print(result)


if __name__ == '__main__':
    repl()
