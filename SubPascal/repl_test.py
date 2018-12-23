from pytest import mark, raises

from dialogue import Dialogue

from repl import repl, multiline_input, QuitRequest
import errors


@mark.parametrize("session, result", [
    ("""
     1|3
     """, '3'),
    ("""
     1|(a
     2| b)
     """, '(a\n b)'),
])
def test_multiline_input(capsys, session, result):
    dlg = Dialogue(session)
    got = multiline_input('1|', '2|', input_fn=dlg.fake_input)
    assert result == got
    captured = capsys.readouterr()
    assert dlg.session == captured.out


@mark.parametrize("session", [
    """
    >Q
    """,
])
def test_multiline_input_quit(session):
    dlg = Dialogue(session)
    with raises(QuitRequest):
        multiline_input('>', quit_cmd='Q', input_fn=dlg.fake_input)


@mark.parametrize("session, error_str", [
    ("""
     )
     """, ')'),
    ("""
     (a
      b))
     """, ' b))'),
    ("""
     (a
      very long line that will be cut))
     """, '…t will be cut))'),
])
def test_multiline_input_unexpected_close_paren(session, error_str):
    dlg = Dialogue(session)
    with raises(errors.UnexpectedCloseParen) as excinfo:
        multiline_input(input_fn=dlg.fake_input)
    assert f"Unexpected close parenthesis: '{error_str}'." == str(excinfo.value)


def test_repl_quit(capsys):
    dlg = Dialogue('> .q\n')
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == captured.out


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
    <UserFunction (mod m n)>
    > (mod 11 4)
    3
    """,
])
def test_repl(capsys, session):
    dlg = Dialogue(session)
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == captured.out


def test_repl_gcd_example(capsys):
    session = """
    > (define mod (m n) (- m (* n (/ m n))))
    <UserFunction (mod m n)>
    > (define gcd (a b) (if (= b 0) a (gcd b (mod a b))))
    <UserFunction (gcd a b)>
    > (gcd 6 15)
    3
    """
    dlg = Dialogue(session)
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == captured.out


def test_repl_gcd_example_multiline(capsys):
    session = """
    > (define not (boolean) (if boolean 0 1))
    <UserFunction (not boolean)>
    > (define <> (x y) (not (= x y)))
    <UserFunction (<> x y)>
    > (define mod (m n) (- m (* n (/ m n))))
    <UserFunction (mod m n)>
    > (define gcd (m n)
    ...  (begin
    ...      (set r (mod m n))
    ...      (while (<> r 0)
    ...           (begin
    ...                (set m n)
    ...                (set n r)
    ...                (set r (mod m n))))
    ... n))
    <UserFunction (gcd m n)>
    > (gcd 42 56)
    14
    """
    dlg = Dialogue(session)
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == captured.out
