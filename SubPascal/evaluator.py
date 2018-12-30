import operator

import errors


VARIADIC = -1  # arity of variadic functions or forms


class ArityCheckerMixin:

    def check_arity(self, args):
        if self.arity == VARIADIC:
            return
        error_type = None
        if len(args) > self.arity:
            error_type = errors.TooManyArguments
        elif len(args) < self.arity:
            error_type = errors.MissingArgument
        if error_type:
            raise error_type(f'{self.name!r} needs {self.arity}')


class Operator(ArityCheckerMixin):

    def __init__(self, name, function, arity):
        self.name = name
        self.function = function
        self.arity = arity

    def __call__(self, *args):
        self.check_arity(args)
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

VALUE_OPS = {op.name: op for op in BUILT_INS}


class SpecialForm(ArityCheckerMixin):

    @property
    def name(self):
        class_name = self.__class__.__name__
        return class_name.replace('Statement', '').lower()

    def __call__(self, environment, *args):
        self.check_arity(args)
        return self.apply(environment, *args)


class SetStatement(SpecialForm):
    arity = 2

    def apply(self, environment, name, val_exp):
        value = evaluate(environment, val_exp)
        if name in environment:
            environment[name] = value
        else:
            global_environment[name] = value
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


CONTROL_OPS = {
    'set': SetStatement(),
    'if': IfStatement(),
    'begin': BeginStatement(),
    'while': WhileStatement(),
}


class UserFunction(ArityCheckerMixin):

    def __init__(self, name, formals, body):
        self.name = name
        self.formals = formals
        self.arity = len(formals)
        self.body = body

    def __repr__(self):
        formals = ' '.join(self.formals)
        return f'<UserFunction ({self.name} {formals})>'

    def __call__(self, *values):
        self.check_arity(values)
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
            try:
                return op(*values)
            except ZeroDivisionError as exc:
                raise errors.DivisionByZero() from exc
