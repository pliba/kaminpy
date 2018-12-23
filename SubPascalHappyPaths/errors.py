class InterpreterException(Exception):
    """Generic interpreter exception."""

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        msg = self.__class__.__doc__
        if self.value is not None:
            msg = msg.rstrip(".")
            msg += ": " + repr(self.value) + "."
        return msg


class UndefinedVariable(InterpreterException):
    """Undefined variable."""


class UndefinedFunction(InterpreterException):
    """Undefined function."""
