import operator
from typing import Dict

from parser import Expression
import errors

VALUE_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}


def let_statement(name: str, exp: Expression) -> int:
    value = evaluate(exp)
    global_environment[name] = value
    return value


global_environment: Dict[str, int] = {}


def evaluate(exp: Expression) -> int:
    """Compute value of expression; return a number."""
    match exp:
        case ['let', var_name, value_exp]:
            return let_statement(var_name, value_exp)
        case [op, *args] if op in VALUE_OPS:
            func = VALUE_OPS[op]
            values = map(evaluate, args)
            return func(*values)
        case symbol if value := global_environment.get(symbol):
            return value
        case atom:
            try:
                return int(atom)
            except ValueError as exc:
                raise errors.UndefinedVariable(atom) from exc

