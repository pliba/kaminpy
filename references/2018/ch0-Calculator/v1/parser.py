class ParsingError(Exception):
    """Generic error while parsing source code."""

    def __str__(self):
        return self.__class__.__doc__


class UnexpectedEndOfSource(ParsingError):
    """Unexpected end of source code."""


class UnexpectedCloseParen(ParsingError):
    """Unexpected ')'."""


def tokenize(source_code):
    """Converter uma string em uma lista de tokens."""
    return source_code.replace("(", " ( ").replace(")", " ) ").split()


def parse(tokens):
    """Construir AST (expressões aninhadas) a partir de uma lista de tokens."""
    try:
        token = tokens.pop(0)
    except IndexError as exc:
        raise UnexpectedEndOfSource() from exc
    if token == "(":  # s-expression
        ast = []
        while tokens and tokens[0] != ")":
            ast.append(parse(tokens))
        if not tokens:
            raise UnexpectedEndOfSource()
        tokens.pop(0)  # drop ')'
        return ast
    elif token == ")":
        raise UnexpectedCloseParen()
    else:
        try:
            return int(token)  # valor numérico
        except ValueError:
            return token  # símbolo
