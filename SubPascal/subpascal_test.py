import io

from pytest import mark

from subpascal import run, env_from_args


def test_run_single_line(capsys):
    source_file = io.StringIO('(print 123)')
    run(source_file)
    captured = capsys.readouterr()
    assert '123\n' == captured.out


def test_run_multiple_lines(capsys):
    source_file = io.StringIO('(print 123)\n(print 456)')
    run(source_file)
    captured = capsys.readouterr()
    assert '123\n456\n' == captured.out


DOUBLING_EXAMPLE = """
(let n 1)
(while (< n 500)
    (begin
        (print n)
        (let n (* n 2))
    )
)
"""


def test_run_doubling_example(capsys):
    source_file = io.StringIO(DOUBLING_EXAMPLE)
    run(source_file)
    captured = capsys.readouterr()
    assert '1\n2\n4\n8\n16\n32\n64\n128\n256\n' == captured.out


GCD_EXAMPLE = """
(define not (boolean) (if boolean 0 1))
(define <> (x y) (not (= x y)))
(define mod (m n) (- m (* n (/ m n))))
(define gcd (m n)
    (begin
        (let r (mod m n))
        (while (<> r 0)
            (begin
                (let m n)
                (let n r)
                (let r (mod m n))))
        n))
(print(gcd 18 35))
"""


def test_run_gcd_example(capsys):
    source_file = io.StringIO(GCD_EXAMPLE)
    run(source_file)
    captured = capsys.readouterr()
    assert '1\n' == captured.out


def test_run_undefined_func_example(capsys):
    source_file = io.StringIO('(spam 18 35)')
    run(source_file)
    captured = capsys.readouterr()
    assert '' == captured.out
    assert "*** Undefined function: 'spam'.\n" == captured.err


def test_run_unexpected_close_paren_example(capsys):
    source_file = io.StringIO('(+ 18 35))')
    run(source_file)
    captured = capsys.readouterr()
    assert '' == captured.out
    assert "*** Unexpected close parenthesis.\n" == captured.err


@mark.parametrize("args, global_env", [
    ([], {}),
    (['x'], {}),
    (['a:2'], {'a': 2}),
    ([':', 'a:-1', 'y:,', 'max:999', '::'], {'a': -1, 'max': 999}),
])
def test_env_from_args(args, global_env):
    got = env_from_args(args)
    assert global_env == got
