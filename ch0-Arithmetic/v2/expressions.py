"""
Simple interpreter implementing the arithmetic expression subset of
the language described in Chapter 1 of Samuel Kamin's PLIBA book [1].
This Python code is heavily inspired by Peter Norvig's lis.py [2],
but does not try to be as concise.

[1] Samuel Kamin, "Programming Languages, An Interpreter-Based Approach",
    Addison-Wesley, Reading, MA, 1990. ISBN 0-201-06824-9.
[2] http://norvig.com/lispy.html

BNF of this mini-language:

<expression> ::= <integer>
               | `(` <operator> <expression>* `)`
<operator>   ::= `+` | `-` | `*` | `/`
<integer>    ::= sequence of digits, possibly preceded by - or +

"""

import operator
import sys

QUIT_COMMAND = '.q'


class InterpreterError(Exception):
    """generic interpreter error"""

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        msg = self.__class__.__doc__
        if self.value is not None:
            msg = msg.rstrip(".")
            msg += ": " + repr(self.value) + "."
        return msg


class UnexpectedEndOfInput(InterpreterError):
    """Unexpected end of input."""


class UnexpectedCloseParen(InterpreterError):
    """Unexpected ')'."""


class UnknownOperator(InterpreterError):
    """Unknown operator."""


class EvaluationError(InterpreterError):
    """Generic evaluation error."""


class OperatorNotCallable(EvaluationError):
    """Operator is not callable."""


class NullExpression(EvaluationError):
    """Null expression."""


class MissingArgument(EvaluationError):
    """Not enough arguments for operator."""


class TooManyArguments(EvaluationError):
    """Too many arguments for operator."""


class InvalidOperator(EvaluationError):
    """Invalid operator."""


def tokenize(source_code):
    """Convert string into a list of tokens."""
    return source_code.replace("(", " ( ").replace(")", " ) ").split()


def parse(tokens):
    """Read tokens building recursively nested expressions."""
    try:
        token = tokens.pop(0)
    except IndexError as exc:
        raise UnexpectedEndOfInput() from exc
    if token == "(":  # s-expression
        ast = []
        if len(tokens) == 0:
            raise UnexpectedEndOfInput()
        while tokens[0] != ")":
            ast.append(parse(tokens))
            if len(tokens) == 0:
                raise UnexpectedEndOfInput()
        tokens.pop(0)  # pop off ')'
        return ast
    elif token == ")":
        raise UnexpectedCloseParen()
    else:  # single atom
        try:
            return int(token)
        except ValueError:
            return token


class Operator:

    def __init__(self, symbol, function, arity):
        self.symbol = symbol
        self.function = function
        self.arity = arity

    def __eq__(self, other):
        return all([self.symbol == other.symbol,
				    self.function == other.function,
				    self.arity == other.arity])

    def eval(self, args):
        needed = self.arity
        if len(args) == needed:
            return self.function(*args)
        elif len(args) < needed:
            raise MissingArgument(self.symbol)
        else:
            raise TooManyArguments(self.symbol)

# In Python 3.7, the inspect.getfullargspec function handles the built-ins abs,
# operator.add, operator.sub, etc. correctly. But in previous versions, we need
# to inform the arity explicitly or provide user-defined functions from which
# inspect.getfullargspec is able to extract the argument specifications.
# For simplicity, I chose to provide de arity.

OPERATORS = [
    Operator("+", operator.add, 2),
    Operator("-", operator.sub, 2),
    Operator("*", operator.mul, 2),
    Operator("/", operator.floordiv, 2),
    Operator("abs", abs, 1),
    Operator("?", lambda cond, a, b: a if cond else b, 3)
]

OPERATOR_MAP = {op.symbol: op for op in OPERATORS}


def evaluate(expression):
    """Compute the value of an expression AST."""
    if isinstance(expression, int):  # integer
        return expression
    elif isinstance(expression, str):  # operator
        try:
            return OPERATOR_MAP[expression]
        except KeyError as exc:
            raise UnknownOperator(expression) from exc
    else:  # multi-part expression
        if len(expression) == 0:
            raise NullExpression()
        parts = [evaluate(subexp) for subexp in expression]
        op = parts.pop(0)
        if isinstance(op, Operator):
            return op.eval(parts)
        else:
            raise InvalidOperator(op)


def repl():
    prompt = '>'
    pending_lines = []
    print(f'To exit, type: {QUIT_COMMAND}', file=sys.stderr)
    while True:
        # ______________________________ Read
        try:
            current = input(prompt + ' ').strip(' ')
        except EOFError:
            break
        if current == QUIT_COMMAND:
            break
        if current == '':
            prompt = '...'
            continue
        pending_lines.append(current)
        # ______________________________ Parse
        source = ' '.join(pending_lines)
        expr = None
        try:
            expr = parse(tokenize(source))
        except UnexpectedEndOfInput:
            prompt = '...'
            continue
        except UnexpectedCloseParen as exc:
            print(f'! {exc}')
        # ______________________________ Evaluate & Print
        if expr is not None:
            try:
                result = evaluate(expr)
            except ZeroDivisionError:
                print('! Division by zero.')
            except (UnknownOperator, InvalidOperator,
                    MissingArgument, TooManyArguments,
                    ) as exc:
                print(f'! {exc}')
            else:
                print(result)
        prompt = '>'
        pending_lines = []
        # ______________________________ Loop


if __name__ == '__main__':
    repl()
