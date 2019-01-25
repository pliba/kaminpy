import operator
from typing import (
    Any, Callable, Dict, List, Optional, Sequence, Type, Union
)

import errors
from parser import Expression

VARIADIC = -1  # arity of variadic functions or forms


def check_arity(form_name: str, arity: int, args: Sequence[Any]):
    if arity == VARIADIC:
        return
    error_type: Optional[Type[errors.EvaluatorException]] = None
    if len(args) > arity:
        error_type = errors.TooManyArguments
    elif len(args) < arity:
        error_type = errors.MissingArgument
    if error_type:
        raise error_type(f'{form_name!r} needs {arity}')


class Operator:

    def __init__(self, name: str, function: Callable, arity: int):
        self.name = name
        self.function = function
        self.arity = arity

    def __call__(self, *args: int) -> int:
        check_arity(self.name, self.arity, args)
        return self.function(*args)


def print_fn(n):
    print(n)
    return n


BUILT_INS = [
    Operator('+', operator.add, 2),
    Operator('-', operator.sub, 2),
    Operator('*', operator.mul, 2),
    Operator('/', operator.floordiv, 2),
    Operator('=', operator.eq, 2),
    Operator('<', operator.lt, 2),
    Operator('>', operator.gt, 2),
    Operator('print', print_fn, 1),
]

OperatorEnv = Dict[str, Operator]

VALUE_OPS: OperatorEnv = {op.name: op for op in BUILT_INS}


class SpecialForm:
    arity: int

    @property
    def name(self):
        class_name = self.__class__.__name__
        return class_name.replace('Statement', '').lower()

    def __call__(self, environment, *args):
        check_arity(self.name, self.arity, args)
        return self.apply(environment, *args)

    def apply(self, *args):
        raise NotImplementedError


class SetStatement(SpecialForm):
    arity = 2

    def apply(self, environment, name, val_exp):
        value = evaluate(environment, val_exp)
        if name in environment:
            environment[name] = value
        else:
            global_env[name] = value
        return value


class IfStatement(SpecialForm):
    arity = 3

    def apply(self, environment, condition, consequence, alternative):
        if evaluate(environment, condition):
            return evaluate(environment, consequence)
        else:
            return evaluate(environment, alternative)


class BeginStatement(SpecialForm):
    arity = VARIADIC

    def apply(self, environment, *statements):
        for statement in statements[:-1]:
            evaluate(environment, statement)
        return evaluate(environment, statements[-1])


class WhileStatement(SpecialForm):
    arity = 2

    def apply(self, environment, condition, block):
        while evaluate(environment, condition):
            evaluate(environment, block)
        return 0


CONTROL_OPS: Dict[str, SpecialForm] = {
    'set': SetStatement(),
    'if': IfStatement(),
    'begin': BeginStatement(),
    'while': WhileStatement(),
}


class UserFunction:

    def __init__(self, name: str, formals: List[str], body: Expression):
        self.name = name
        self.formals = formals
        self.arity = len(formals)
        self.body = body

    def __repr__(self):
        formals = ' '.join(self.formals)
        return f'<UserFunction ({self.name} {formals})>'

    def __call__(self, *values):
        check_arity(self.name, self.arity, values)
        local_env = dict(zip(self.formals, values))
        return evaluate(local_env, self.body)


ValueEnv = Dict[str, int]
FunctionEnv = Dict[str, UserFunction]

global_env: ValueEnv = {}
function_env: FunctionEnv = {}


def define_function(parts):
    name, formals, body = parts
    user_fn = UserFunction(name, formals, body)
    function_env[name] = user_fn
    return repr(user_fn)


def fetch_variable(env: ValueEnv, name: str) -> int:
    try:
        return env[name]
    except KeyError:
        try:
            return global_env[name]
        except KeyError as exc:
            raise errors.UndefinedVariable(name) from exc


Function = Union[Operator, UserFunction]


def fetch_function(name: str) -> Function:
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
            try:
                return op(*values)
            except ZeroDivisionError as exc:
                raise errors.DivisionByZero() from exc
