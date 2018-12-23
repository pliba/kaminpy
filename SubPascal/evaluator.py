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


class UserFunction:

    def __init__(self, name, formals, body):
        self.name = name
        self.formals = formals
        self.body = body

    def __repr__(self):
        formals = ', '.join(self.formals)
        return f'<UserFunction {self.name}({formals})>'

    def __call__(self, *values):
        local_env = dict(zip(self.formals, values))
        return evaluate(local_env, self.body)


def define_function(parts):
    name, formals, body = parts
    user_fn = UserFunction(name, formals, body)
    function_definitions[name] = user_fn
    return repr(user_fn)


global_environment = {}

function_definitions = {}


def fetch_variable(environment, name):
    try:
        return environment[name]
    except KeyError:
        try:
            return global_environment[name]
        except KeyError as exc:
            raise errors.UndefinedVariable(name) from exc


def fetch_function(name):
    try:
        return VALUE_OPS[name]
    except KeyError:
        try:
            return function_definitions[name]
        except KeyError as exc:
            raise errors.UndefinedFunction(name) from exc


def evaluate(environment, expression):
    """Given an environment, evaluate expression."""

    if isinstance(expression, int):  # number
        return expression

    if isinstance(expression, str):  # variable
        return fetch_variable(environment, expression)

    else:  # application expression
        op_name = expression[0]
        args = expression[1:]
        if op_name in CONTROL_OPS:
            op = CONTROL_OPS[op_name]
            return op(environment, *args)
        else:
            op = fetch_function(op_name)
            values = (evaluate(environment, x) for x in args)
            return op(*values)
