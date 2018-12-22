import errors

global_environment = {}


def evaluate(expression, environment):
    """Evaluate expression in environment, return its value (a number)."""

    if isinstance(expression, int):
        return expression
    else:
        try:
            return environment[expression]
        except KeyError:
            try:
                return global_environment[expression]
            except KeyError as exc:
                raise errors.UndefinedVariable(expression) from exc
