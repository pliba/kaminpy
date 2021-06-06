import operator

from parser import Expression

VALUE_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}

def evaluate(exp: Expression) -> int:
    """Evaluate expression, return its value (a number)."""
    match exp:
        case [op, *args] if op in VALUE_OPS:
            func = VALUE_OPS[op]
            values = map(evaluate, args)
            return func(*values)
        case atom:
            return float(atom)
