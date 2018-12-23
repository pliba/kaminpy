import operator


VALUE_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}


def evaluate(expression, environment):
    """Evaluate expression in environment, return its value (a number)."""

    if isinstance(expression, int):  # number
        return expression
    else:  # application expression
        op_name = expression[0]
        op = VALUE_OPS[op_name]
        args = expression[1:]
        values = (evaluate(x, environment) for x in args)
        return op(*values)
