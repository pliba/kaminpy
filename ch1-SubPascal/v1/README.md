# Pascal subset interpreter -- v1

This version adds support for `print` and `begin` commands.

Example:

```
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
``` 
