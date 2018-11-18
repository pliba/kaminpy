import operator
import textwrap

from pytest import mark, raises

from .test_expressions import TextInteraction

from .subpascal import repl


@mark.parametrize("session", [
    """
    > (set x 3)
    3
    > x
    3
    > (* x 4)
    12
    """,
])
def test_set_command(monkeypatch, capsys, session):
    ti = TextInteraction(session)
    with monkeypatch.context() as m:
        m.setitem(__builtins__, "input", ti.fake_input)
        repl()
    captured = capsys.readouterr()
    assert captured.out == str(ti)


@mark.parametrize("session", [
    """
    > (print 3)
    3
    3
    """,
])
def test_print_command(monkeypatch, capsys, session):
    ti = TextInteraction(session)
    with monkeypatch.context() as m:
        m.setitem(__builtins__, "input", ti.fake_input)
        repl()
    captured = capsys.readouterr()
    assert captured.out == str(ti)


@mark.parametrize("session", [
    """
    > (begin
    ... (set a 2)
    ... (set b 3)
    ... (* a b)
    ... )
    6
    > (begin
    ... (print 1)
    ... (print 2)
    ... (print 3)
    ... )
    1
    2
    3
    3
    """,
])
def test_begin_command(monkeypatch, capsys, session):
    ti = TextInteraction(session)
    with monkeypatch.context() as m:
        m.setitem(__builtins__, "input", ti.fake_input)
        repl()
    captured = capsys.readouterr()
    assert str(ti) == captured.out
