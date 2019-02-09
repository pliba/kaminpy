import operator


VALUE_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}


def evaluate(expression):
    """Evaluate expression, return its value (a number)."""

    if isinstance(expression, int):  # number
        return expression
    else:  # application expression
        op_name = expression[0]
        op = VALUE_OPS[op_name]
        args = expression[1:]
        values = []
        for x in args:
            values.append(evaluate(x))
        return op(*values)


def demo():
    from parser import tokenize, parse_exp
    source = '(* 6 (+ 3 4))'
    tokens = tokenize(source)
    expr = parse_exp(tokens)
    result = evaluate(expr)
    print(result)

demo()
