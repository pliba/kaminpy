from pytest import mark

from .test_expressions import TextInteraction

from .subpascal import repl, tokenize, parse, evaluate


@mark.parametrize("session", [
    """
    > (set x 3)
    3
    > x
    3
    > (* x 4)
    12
    > (set x (* x 5))
    15
    > x
    15
    """,
])
def test_set_session(monkeypatch, capsys, session):
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
def test_print_session(monkeypatch, capsys, session):
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
def test_begin_session(monkeypatch, capsys, session):
    ti = TextInteraction(session)
    with monkeypatch.context() as m:
        m.setitem(__builtins__, "input", ti.fake_input)
        repl()
    captured = capsys.readouterr()
    assert str(ti) == captured.out


@mark.parametrize("session", [
    """
    > (if (< 10 20) 1 2)
    1
    > (if (> 10 20) 1 2)
    2
    """,
])
def test_if_session(monkeypatch, capsys, session):
    ti = TextInteraction(session)
    with monkeypatch.context() as m:
        m.setitem(__builtins__, "input", ti.fake_input)
        repl()
    captured = capsys.readouterr()
    assert str(ti) == captured.out


def test_while_command():
    source = """
    (begin
      (set x 2)
      (while (> x 0)
        (set x (- x 1))
      )
    )  
    """
    expr = parse(tokenize(source))
    want = ['begin',
             ['set', 'x', 2],
             ['while', ['>', 'x', 0],
                ['set', 'x', ['-', 'x', 1]]]]

    assert want == expr
    assert 0 == evaluate(expr)


@mark.parametrize("session", [
    """
    > (set x 3)
    3
    > (while (> x 0)
    ... (begin
    ...    (print x)
    ...    (set x (- x 1))
    ... ))
    3
    2
    1
    0
    """,
])
def test_while_session(monkeypatch, capsys, session):
    ti = TextInteraction(session)
    with monkeypatch.context() as m:
        m.setitem(__builtins__, "input", ti.fake_input)
        repl()
    captured = capsys.readouterr()
    assert str(ti) == captured.out
