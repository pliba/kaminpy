import operator
from typing import TypeAlias

import errors

def divide(a, b):
    q = a / b
    i = int(q)
    return i if i == q else q

VALUE_OPS = {
    '+': lambda *args: sum(args),
    '-': operator.sub,
    '*': operator.mul,
    '/': divide,
}

Number: TypeAlias = int | float
Atom: TypeAlias = str | Number
Expression: TypeAlias = Atom | list

global_env: dict[str, int] = {}

def evaluate(exp: Expression) -> Number:
    """Compute value of expression; return a number."""
    match exp:
        case int() | float():
            return exp
        case ['let', name, exp]:
            value = evaluate(exp)
            global_env[name] = value
            return value
        case [op, *args] if func := VALUE_OPS.get(op):
            values = map(evaluate, args)
            return func(*values)
        case variable if (value := global_env.get(variable)) is not None:
            return value
        case _:
            raise errors.UndefinedVariable(exp)
