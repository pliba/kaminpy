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

    if isinstance(exp, int):  # number
        return exp
    else:  # application expression
        op_name = exp[0]
        op = VALUE_OPS[op_name]
        args = exp[1:]
        values = (evaluate(x) for x in args)
        return op(*values)
