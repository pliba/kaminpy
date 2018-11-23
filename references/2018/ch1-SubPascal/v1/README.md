# Pascal subset interpreter -- v1

This is an interpreter for a very small subset of Pascal using s-expression syntax.

Example:

```
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
``` 
