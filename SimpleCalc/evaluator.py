def tokenize(source):
    spaced = source.replace('(', ' ( ').replace(')', ' ) ')
    return spaced.split()


OPERATORS = {
    '+': lambda *args: sum(args),
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
}


def evaluate(tokens):
    head = tokens.pop(0)
    if head == '(':
        op = OPERATORS[tokens.pop(0)]
        args = []
        while tokens and tokens[0] != ')':
            args.append(evaluate(tokens))
        tokens.pop(0)  # drop ')'
        return op(*args)
    else:
        return float(head)


QUIT_COMMAND = '.q'


def repl():
    """Read-Eval-Print-Loop"""
    print(f'To exit, type {QUIT_COMMAND}')

    while True:
        line = input('> ')                 # Read
        if line == QUIT_COMMAND:
            break
        value = evaluate(tokenize(line))   # Eval
        print(value)                       # Print
