import operator
from typing import TypeAlias

VALUE_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}

Atom: TypeAlias = str | float
Expression: TypeAlias = Atom | list

def evaluate(exp: Expression) -> float:
    """Compute value of expression; return a number."""
    match exp:
        case [op, *args] if op in VALUE_OPS:
            func = VALUE_OPS[op]
            values = map(evaluate, args)
            return func(*values)
        case float():
            return exp
        case int():
            return float(exp)
