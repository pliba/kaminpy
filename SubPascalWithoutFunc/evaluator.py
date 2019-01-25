import operator
from typing import Callable, Dict

import errors
from parser import Expression


def print_fn(n):
    print(n)
    return n


OperatorEnv = Dict[str, Callable[..., int]]

VALUE_OPS: OperatorEnv = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
    '=': operator.eq,
    '<': operator.lt,
    '>': operator.gt,
    'print': print_fn,
}


def set_statement(environment, name, val_exp):
    value = evaluate(environment, val_exp)
    if name in environment:
        environment[name] = value
    else:
        global_env[name] = value
    return value


def if_statement(environment, condition, consequence, alternative):
    if evaluate(environment, condition):
        return evaluate(environment, consequence)
    else:
        return evaluate(environment, alternative)


def begin_statement(environment, *statements):
    for statement in statements[:-1]:
        evaluate(environment, statement)
    return evaluate(environment, statements[-1])


def while_statement(environment, condition, block):
    while evaluate(environment, condition):
        evaluate(environment, block)
    return 0


CONTROL_OPS: Dict[str, Callable[..., int]] = {
    'set': set_statement,
    'if': if_statement,
    'begin': begin_statement,
    'while': while_statement,
}


ValueEnv = Dict[str, int]

global_env: ValueEnv = {}


def evaluate(env: ValueEnv, exp: Expression) -> int:
    """Given an environment, evaluate expression."""

    if isinstance(exp, int):  # number
        return exp

    if isinstance(exp, str):  # variable
        try:
            return env[exp]
        except KeyError:
            try:
                return global_env[exp]
            except KeyError as exc:
                raise errors.UndefinedVariable(exp) from exc

    else:  # application expression
        op_name = exp[0]
        args = exp[1:]
        if op_name in CONTROL_OPS:
            statement = CONTROL_OPS[op_name]
            return statement(env, *args)
        else:
            op = VALUE_OPS[op_name]
            values = tuple(evaluate(env, x) for x in args)
            return op(*values)
