import operator

import errors


VALUE_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}


def set_statement(name, val_exp):
    value = evaluate(val_exp)
    global_environment[name] = value
    return value


global_environment = {}


def evaluate(expression):
    """Evaluate expression, return its value (a number)."""

    if isinstance(expression, int):  # number
        return expression

    if isinstance(expression, str):  # variable
        try:
            return global_environment[expression]
        except KeyError as exc:
            raise errors.UndefinedVariable(expression) from exc

    else:  # application expression
        op_name = expression[0]
        args = expression[1:]
        if op_name == 'set':
            name, val_exp = args
            return set_statement(name, val_exp)
        else:
            op = VALUE_OPS[op_name]
            values = (evaluate(x) for x in args)
            return op(*values)
