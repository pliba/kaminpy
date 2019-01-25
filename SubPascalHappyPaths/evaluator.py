import operator
from typing import Callable, Dict, List

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


class UserFunction:

    def __init__(self, name: str, formals: List[str], body: Expression):
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
    function_env[name] = user_fn
    return repr(user_fn)


ValueEnv = Dict[str, int]
FunctionEnv = Dict[str, UserFunction]

global_env: ValueEnv = {}
function_env: FunctionEnv = {}


def fetch_variable(environment, name):
    try:
        return environment[name]
    except KeyError:
        try:
            return global_env[name]
        except KeyError as exc:
            raise errors.UndefinedVariable(name) from exc


def fetch_function(name):
    try:
        return VALUE_OPS[name]
    except KeyError:
        try:
            return function_env[name]
        except KeyError as exc:
            raise errors.UndefinedFunction(name) from exc


def evaluate(env: ValueEnv, exp: Expression) -> int:
    """Given an environment, evaluate expression."""

    if isinstance(exp, int):  # number
        return exp

    if isinstance(exp, str):  # variable
        return fetch_variable(env, exp)

    else:  # application expression
        op_name = exp[0]
        args = exp[1:]
        if op_name in CONTROL_OPS:
            statement = CONTROL_OPS[op_name]
            return statement(env, *args)
        else:
            op = fetch_function(op_name)
            values = tuple(evaluate(env, x) for x in args)
            return op(*values)
