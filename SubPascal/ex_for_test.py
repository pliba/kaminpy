import io

from pytest import mark

from subpascal import run, env_from_args

SERIES_EXAMPLE = """
(set n 5)
(for i 1 n (print i))
"""


def test_run_doubling_example(capsys):
    source_file = io.StringIO(SERIES_EXAMPLE)
    run(source_file)
    captured = capsys.readouterr()
    assert '' == captured.err
    assert '1\n2\n3\n4\n5\n' == captured.out
