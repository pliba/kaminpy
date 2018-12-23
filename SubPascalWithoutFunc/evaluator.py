import operator

import errors


def print_fn(n):
    print(n)
    return n


VALUE_OPS = {
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
        global_environment[name] = value
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


CONTROL_OPS = {
    'set': set_statement,
    'if': if_statement,
    'begin': begin_statement,
    'while': while_statement,
}

global_environment = {}


def evaluate(environment, expression):
    """Given an environment, evaluate expression."""

    if isinstance(expression, int):  # number
        return expression

    if isinstance(expression, str):  # variable
        try:
            return environment[expression]
        except KeyError:
            try:
                return global_environment[expression]
            except KeyError as exc:
                raise errors.UndefinedVariable(expression) from exc

    else:  # application expression
        op_name = expression[0]
        args = expression[1:]
        if op_name in CONTROL_OPS:
            op = CONTROL_OPS[op_name]
            return op(environment, *args)
        else:
            op = VALUE_OPS[op_name]
            values = (evaluate(environment, x) for x in args)
            return op(*values)
