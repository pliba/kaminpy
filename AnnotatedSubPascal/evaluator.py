import operator
from typing import Mapping, Callable, List, Any, Optional, Type, Tuple

import errors
from parser import Symbol, Number, Expression


Environment = Mapping[Symbol, Number]
FunctionEnv = Mapping[Symbol, Callable]


VARIADIC = -1  # arity of variadic functions or forms


def check_arity(form_name: Symbol, arity: int, args: Tuple[Any, ...]):
    if arity == VARIADIC:
        return
    error_type: Optional[Type[Exception]] = None
    if len(args) > arity:
        error_type = errors.TooManyArguments
    elif len(args) < arity:
        error_type = errors.MissingArgument
    if error_type:
        raise error_type(f'{form_name!r} needs {arity}')


class Operator:

    def __init__(self, name: Symbol, function: Callable, arity: int):
        self.name = name
        self.function = function
        self.arity = arity

    def __call__(self, *args: List[Number]) -> Number:
        check_arity(self.name, self.arity, args)
        return self.function(*args)


def print_fn(n):
    print(n)
    return n


BUILT_INS = [
    Operator(Symbol('+'), operator.add, 2),
    Operator(Symbol('-'), operator.sub, 2),
    Operator(Symbol('*'), operator.mul, 2),
    Operator(Symbol('/'), operator.floordiv, 2),
    Operator(Symbol('='), operator.eq, 2),
    Operator(Symbol('<'), operator.lt, 2),
    Operator(Symbol('>'), operator.gt, 2),
    Operator(Symbol('print'), print_fn, 1),
]

VALUE_OPS: FunctionEnv = {op.name: op for op in BUILT_INS}


class Statement:

    arity: int

    @property
    def name(self) -> Symbol:
        class_name = self.__class__.__name__
        return Symbol(class_name.replace('Statement', '').lower())

    def __call__(self, env: Environment, *args: Tuple[Any, ...]) -> Number:
        check_arity(self.name, self.arity, args)
        return self.apply(env, *args)

    def apply(self, *args):
        raise NotImplementedError


class SetStatement(Statement):
    arity = 2

    def apply(self, environment, name, val_exp):
        value = evaluate(environment, val_exp)
        if name in environment:
            environment[name] = value
        else:
            global_environment[name] = value
        return value


class IfStatement(Statement):
    arity = 3

    def apply(self, environment, condition, consequence, alternative):
        if evaluate(environment, condition):
            return evaluate(environment, consequence)
        else:
            return evaluate(environment, alternative)


class BeginStatement(Statement):
    arity = VARIADIC

    def apply(self, environment, *statements):
        for statement in statements[:-1]:
            evaluate(environment, statement)
        return evaluate(environment, statements[-1])


class WhileStatement(Statement):
    arity = 2

    def apply(self, environment, condition, block):
        while evaluate(environment, condition):
            evaluate(environment, block)
        return 0


StatementEnv = Mapping[Symbol, Statement]

CONTROL_OPS: StatementEnv = {
    Symbol('set'): SetStatement(),
    Symbol('if'): IfStatement(),
    Symbol('begin'): BeginStatement(),
    Symbol('while'): WhileStatement(),
}


class UserFunction:

    def __init__(self, name, formals, body):
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


def define_function(parts):
    name, formals, body = parts
    user_fn = UserFunction(name, formals, body)
    function_definitions[name] = user_fn
    return repr(user_fn)


global_environment: Environment = {}

function_definitions: FunctionEnv = {}


def fetch_variable(env: Environment, name: Symbol) -> Number:
    try:
        return env[name]
    except KeyError:
        try:
            return global_environment[name]
        except KeyError as exc:
            raise errors.UndefinedVariable(name) from exc


def fetch_function(name: Symbol) -> Callable:
    try:
        return VALUE_OPS[name]
    except KeyError:
        try:
            return function_definitions[name]
        except KeyError as exc:
            raise errors.UndefinedFunction(name) from exc


def evaluate(env: Environment, exp: Expression) -> Number:
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
            values = (evaluate(env, x) for x in args)
            try:
                return op(*values)
            except ZeroDivisionError as exc:
                raise errors.DivisionByZero() from exc
