from pytest import mark, approx

from dialogue import Dialogue

from calc import evaluate, repl, format_stack


@mark.parametrize("source, want", [
    ('2', 2),
    ('2 3 +', 5),
    ('5 3 -', 2),
    ('3 5 * 2 +', 17),
    ('100 32 - 5 * 9 /', approx(37.7, .01)),
])
def test_evaluate(source, want):
    stack = [] 
    got = evaluate(source.split(), stack)
    assert want == got


@mark.parametrize("value, want", [
    ([], '[]'),
    ([3], '[3]'),
    ([3, 4, 5], '3 4 [5]'),
])
def test_format_stack(value, want):
    assert want == format_stack(value)


@mark.parametrize("session", [
    """
    > 3
    [3.0]
    """,
    """
    > 3 5 6
    3.0 5.0 [6.0]
    > *
    3.0 [30.0]
    > -
    [-27.0]
    """,
])
def test_repl(capsys, session):
    dlg = Dialogue(session)
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session.strip() == captured.out.strip()
