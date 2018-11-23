import collections
import operator


class EvaluationError(Exception):
    """Error while evaluating expression."""

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        msg = self.__class__.__doc__
        if self.value is not None:
            msg = msg.rstrip(".")
            msg += ": " + repr(self.value) + "."
        return msg


class InvalidExpression(EvaluationError):
    """Invalid expression."""


class InvalidOperator(EvaluationError):
    """Invalid operator."""


class MissingArgument(EvaluationError):
    """Missing argument."""


Operator = collections.namedtuple("Operator", "symbol function")

OPERATORS = [
    Operator("+", operator.add),
    Operator("-", operator.sub),
    Operator("*", operator.mul),
    Operator("/", operator.floordiv),
]

BUILTINS = {op.symbol: op for op in OPERATORS}


def evaluate(expression):
    """Computar o valor da expression.

    Expression é um AST: valores simples ou listas aninhadas
    representando uma expressão.
    """
    if isinstance(expression, int):  # valor numérico
        return expression
    elif isinstance(expression, str):  # símbolo
        return BUILTINS[expression]
    elif isinstance(expression, list):  # s-expression
        head = evaluate(expression[0])
        if isinstance(head, Operator):
            args = (evaluate(e) for e in expression[1:])
            return head.function(*args)
        else:
            raise InvalidOperator(expression[0])

    else:
        raise InvalidExpression()
