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
import collections

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


class UnknownSymbol(InterpreterError):
    """Unknown symbol."""


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


def unary_print(x):
    print(x)
    return x


OPERATORS = [
    Operator("+", operator.add, 2),
    Operator("-", operator.sub, 2),
    Operator("*", operator.mul, 2),
    Operator("/", operator.floordiv, 2),
    Operator("=", operator.eq, 2),
    Operator("!=", operator.ne, 2),
    Operator(">", operator.gt, 2),
    Operator(">=", operator.ge, 2),
    Operator("<", operator.lt, 2),
    Operator("<=", operator.le, 2),
    Operator("abs", abs, 1),
    Operator("?", lambda cond, a, b: a if cond else b, 3),
    Operator("print", unary_print, 1),
]

OPERATOR_MAP = {op.symbol: op for op in OPERATORS}

global_vars = {}


def command_set(symbol, value_expr):
    value = evaluate(value_expr)
    global_vars[symbol] = value
    return value


def command_begin(*statements):
    for statement in statements[:-1]:
        evaluate(statement)
    return evaluate(statements[-1])


def command_if(condition, consequence, alternative):
    if evaluate(condition):
        return evaluate(consequence)
    else:
        return evaluate(alternative)


def command_while(condition, block):
    while evaluate(condition):
        result = evaluate(block)
    return result


Command = collections.namedtuple('Command', 'symbol function')

COMMANDS = [
    Command('set', command_set),
    Command('begin', command_begin),
    Command('if', command_if),
    Command('while', command_while),
]

COMMAND_MAP = {cmd.symbol: cmd for cmd in COMMANDS}


def evaluate(expression):
    """Compute the value of an expression AST."""
    if isinstance(expression, int):  # integer
        return expression
    elif isinstance(expression, str):  # operator
        symbol = expression
        try:
            return COMMAND_MAP[symbol]
        except KeyError:
            try:
                return global_vars[symbol]
            except KeyError:
                try:
                    return OPERATOR_MAP[symbol]
                except KeyError as exc:
                    raise UnknownSymbol(symbol) from exc
    else:  # multi-part expression
        if len(expression) == 0:
            raise NullExpression()
        op = evaluate(expression[0])
        expression = expression[1:]
        if isinstance(op, Command):
            return op.function(*expression)
        if isinstance(op, Operator):
            args = [evaluate(subexp) for subexp in expression]
            return op.eval(args)
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
            except (UnknownSymbol, InvalidOperator,
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
