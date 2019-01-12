from pytest import mark, approx

from dialogue import Dialogue

from evaluator import tokenize, evaluate, repl


@mark.parametrize("source, want", [
    ('3', ['3']),
    ('abs', ['abs']),
    ('(now)', ['(', 'now', ')']),
    ('()', ['(', ')']),
    ('(+ 2   3)', ['(', '+', '2', '3', ')']),
    ('(+ 2 (* 3 5))', ['(', '+', '2', '(', '*', '3', '5', ')', ')']),
])
def test_tokenize(source, want):
    tokens = tokenize(source)
    assert want == tokens


@mark.parametrize("source, want", [
    ('2', 2),
    ('(+ 2 3)', 5),
    ('(+ 1 2 3 4)', 10),
    ('(+ 2 (* 3 5))', 17),
    ('(/ (* (- 100 32) 5) 9)', approx(37.7, .01)),
])
def test_evaluate(source, want):
    result = evaluate(tokenize(source))
    assert want == result


@mark.parametrize("session", [
    """
    > .q
    """,
    """
    > .q
    """,
    """
    > 3
    3.0
    > .q
    """,
    """
    > (+ 1 2 3 4)
    10.0
    > .q
    """,
])
def test_repl_quit_other_cases(capsys, session):
    dlg = Dialogue(session)
    repl(dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == captured.out
