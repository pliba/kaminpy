################ Lispy: Scheme Interpreter in Python 3.10   

## (c) Peter Norvig, 2010-18; See http://norvig.com/lispy.html
## Ported to Python 3.10 with Pattern Matching by Luciano Ramalho

################ Imports and Types

import math
import operator as op
from collections import ChainMap as Environment

Symbol = str          # A Lisp Symbol is implemented as a Python str
List   = list         # A Lisp List   is implemented as a Python list
Number = (int, float) # A Lisp Number is implemented as a Python int or float

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        env =  Environment(dict(zip(self.parms, args)), self.env)
        return evaluate(self.body, env)

################ Global Environment

def standard_env():
    "An environment with some Scheme standard procedures."
    env = {}
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     lambda *args: list(map(*args)),
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

################ Interaction: A REPL

def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = evaluate(parse(input(prompt)))
        if val is not None:
            print(lispstr(val))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(lispstr, exp)) + ')' 
    else:
        return str(exp)

################ evaluate

def evaluate(x, env=global_env):
    match x:
        case Symbol():                                # variable reference
            return env[x]
        case literal if not isinstance(x, List):      # constant literal
            return literal
        case ['quote', exp]:                          # (quote exp)
            return exp
        case ['if', test, conseq, alt]:               # (if test conseq alt)
            exp = conseq if evaluate(test, env) else alt
            return evaluate(exp, env)
        case ['define', var, exp]:                    # (define var exp)
            env[var] = evaluate(exp, env)
        case ['lambda', parms, body]:                 # (lambda (var...) body)
            return Procedure(parms, body, env)
        case [op, *args]:                             # (proc arg...)
            proc = evaluate(op, env)
            values = (evaluate(arg, env) for arg in args)
            return proc(*values)
