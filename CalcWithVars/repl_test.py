from pytest import mark

from dialogue import Dialogue, normalize

from repl import repl


def test_repl_quit(capsys):
    dlg = Dialogue('> .q\n')
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


@mark.parametrize("session", [
    """
    >
    > .q
    """,
    """
    > 3
    3
    > .q
    """,
    """
    > 3.5
    3.5
    """,
    """
    > (/ 1 8)
    0.125
    > (* (+ 2 4) (- 10 3))
    42
    > (/ (* (- 104 32) 5) 9)
    40
    > (/ (* (- 104.9 32) 5) 9)
    40.5
    """,
    """
    > x
    *** Undefined variable: 'x'.
    """,
    """
    > (let x 3.1416)
    3.1416
    > x
    3.1416
    > (let n (* 4 2))
    8
    > (* n n)
    64
    """,
])
def test_repl(capsys, session):
    dlg = Dialogue(session)
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)
