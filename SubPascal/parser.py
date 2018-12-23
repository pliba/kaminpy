#!/usr/bin/env python3

import collections


def tokenize(source):
    spaced = source.replace('(', ' ( ').replace(')', ' ) ')
    return collections.deque(spaced.split())


def parse_token(token):
    if token[0] == '+':
        return token
    try:
        return int(token)
    except ValueError:
        return token


def parse_exp(tokens):
    head = tokens.popleft()
    if head == '(':
        ast = []
        while tokens[0] != ")":
            ast.append(parse_exp(tokens))
        tokens.popleft()  # drop ')'
        return ast
    else:
        return parse_token(head)


if __name__ == '__main__':
    import sys
    print(parse_exp(tokenize(sys.stdin.read())))
