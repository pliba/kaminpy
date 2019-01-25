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


def set_statement(name: str, exp: Expression) -> int:
    value = evaluate(exp)
    global_environment[name] = value
    return value


global_environment: Dict[str, int] = {}


def evaluate(exp: Expression) -> int:
    """Evaluate expression, return its value (a number)."""

    if isinstance(exp, int):  # number
        return exp

    if isinstance(exp, str):  # variable
        try:
            return global_environment[exp]
        except KeyError as exc:
            raise errors.UndefinedVariable(exp) from exc

    else:  # application expression
        op_name = exp[0]
        args = exp[1:]
        if op_name == 'set':
            name, val_exp = args
            return set_statement(name, val_exp)
        else:
            op = VALUE_OPS[op_name]
            values = (evaluate(x) for x in args)
            return op(*values)
