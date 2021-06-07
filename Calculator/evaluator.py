import operator
from typing import TypeAlias

def divide(a, b):
    q = a / b
    i = int(q)
    return i if i == q else q

VALUE_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': divide,
}

Number: TypeAlias = int | float
Atom: TypeAlias = str | Number
Expression: TypeAlias = Atom | list

def evaluate(exp: Expression) -> Number:
    """Compute value of expression; return a number."""
    match exp:
        case [op, *args] if op in VALUE_OPS:
            func = VALUE_OPS[op]
            values = map(evaluate, args)
            return func(*values)
        case int() | float():
            return exp
