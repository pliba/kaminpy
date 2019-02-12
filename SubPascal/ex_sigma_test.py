from pytest import mark

import io

import parser
import subpascal

sigma_src = """
    (define sigma (m n) 
        (if (>= (- n 1) m) 
            (+ (sigma m (- n 1 )) n)
            m
        )
    )
"""

@mark.parametrize("src, output", [
    ('(print (sigma 0 0))', '0\n'),
    ('(print (sigma 5 5))', '5\n'),
    ('(print (sigma 0 1))', '1\n'),
    ('(print (sigma 0 2))', '3\n'),
    ('(print (sigma 1 2))', '3\n'),
    ('(print (sigma 3 7))', '25\n'),
])
def test_sigma_recursive(capsys, src, output):
    src = sigma_src + '\n' + src
    source_file = io.StringIO(src)
    subpascal.run(source_file)
    captured = capsys.readouterr()
    assert '' == captured.err
    assert output == captured.out


sigma_while_src = """
(define sigma (m n) (begin
    (set total 0)
    (while (>= n m) (begin
        (set total (+ total n))
        (set n (- n 1))
    ))
    total
))
"""


@mark.parametrize("src, output", [
    ('(print (sigma 0 0))', '0\n'),
    ('(print (sigma 5 5))', '5\n'),
    ('(print (sigma 0 1))', '1\n'),
    ('(print (sigma 0 2))', '3\n'),
    ('(print (sigma 1 2))', '3\n'),
    ('(print (sigma 3 7))', '25\n'),
])
def test_sigma_iterative(capsys, src, output):
    src = sigma_while_src + '\n' + src
    source_file = io.StringIO(src)
    subpascal.run(source_file)
    captured = capsys.readouterr()
    assert '' == captured.err
    assert output == captured.out
