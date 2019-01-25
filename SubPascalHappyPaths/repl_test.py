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
    > 3
    3
    """,
    """
    > (* (+ 2 4) (- 10 3))
    42
    > (/ (* (- 100 32) 5) 9)
    37
    """,
    """
    > x
    *** Undefined variable: 'x'.
    """,
    """
    > (set n (* 4 2))
    8
    > (* n n)
    64
    """,
    """
    > (define mod (m n) (- m (* n (/ m n))))
    <UserFunction mod(m, n)>
    > (mod 11 4)
    3
    """,
])
def test_repl(capsys, session):
    dlg = Dialogue(session)
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


def test_repl_gcd_example(capsys):
    session = """
    > (define mod (m n) (- m (* n (/ m n))))
    <UserFunction mod(m, n)>
    > (define gcd (a b) (if (= b 0) a (gcd b (mod a b))))
    <UserFunction gcd(a, b)>
    > (gcd 6 15)
    3
    """
    dlg = Dialogue(session)
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)
