# SubPascal

This is a Python implementation of the small language described in chapter 1 of *Programming Languages, An Interpreter-Based Approach* by Samuel Kamin. Kamin calls it *chapter 1 language*. I call it **SubPascal**.
 
**SubPascal** is [Turing Complete](https://en.wikipedia.org/wiki/Turing_completeness), but very simple: it is written in *s-expression* syntax and integers are the only supported data type.

Here is the greatest common divisor iterative algorithm in **SubPascal**:

```lisp
(define <> (x y) (if (= x y) 0 1))
(define mod (m n) (- m (* n (/ m n))))
(define gcd (m n)
    (begin
        (set r (mod m n))
        (while (<> r 0)
            (begin
                (set m n)
                (set n r)
                (set r (mod m n))))
        n
    )
)
(gcd 6 15)
3
```

## Interactive use

Running `subpascal.py` without arguments opens a REPL. You can do integer arithmetic and define functions, like a recursive `gcd`:

```
$ ./subpascal.py
To exit, type .q
> (* 11111 11111)                       
123454321
> (define mod (m n) (- m (* n (/ m n))))
<UserFunction (mod m n)>
> (define gcd (m n)
... (if (= n 0) m (gcd n (mod m n))))
<UserFunction (gcd m n)>
> (gcd 95 38)
19
> 
```

## Command-line integration

A **Sub-Pascal** function like `gcd` can be turned in to a command-line script by replacing the constants in the last line with variables that the user can provide via the command line, and adding a call to `print`, to display the result.

This is the `gcd-a-b.subpas` script:

```lisp
(define mod (m n)
    (- m (* n (/ m n))))

(define gcd (m n)
    (if (= n 0)
        m
        (gcd n (mod m n))))

(print (gcd a b))
```

To run it, provide the values for the `a` and `b` variables in the command-line, like this:

```
$ ./subpascal.py gcd-a-b.subpas a:18 b:45
9
```

If you forget to provide the required arguments, the interpreter will complain (but currently it stops at the first issue found):

```
$ ./subpascal.py gcd-a-b.subpas
*** Undefined variable: 'a'.
```


## SubPascal Syntax

### `(f e₁ e₂ e₃ …)`

**Function application**: the expressions `e₁`, `e₂`, `e₃`, etc. are evaluated, and the `f` function is applied to them.

Note that **SubPascal** operators are functions named `+`, `/`, `=`, `>`, etc. For example, `(* 2 3)` returns 6, and the value of `(> 3 5)` is 0 (false).

### `(if e₁ e₂ e₃)`

**Conditional**: `e₁` is evaluated, and will be considered *false* if it is 0, any other value is *true*. If `e₁` is *true*, then `e₂` will be evaluated; otherwise,  `e₃` will be evaluated. Note that the  `if` command only evaluates 2 of its 3 arguments. In contrast, a **function application** always evaluates all its arguments before the function itself is executed.

The value of a complete `if` expression is the value of the consequence `e₂` or the alternative `e₃`.

### `(set x e)`

**Variable binding**: the `e` expression is evaluated and its value assigned to variable `x`. Note that the first argument `x` is not evaluated — it is just the name of the variable. To increment a variable `x`, you'd write `(set x (+ x 1))`.

The value of a complete `set` expression is the value assigned to the variable.

### `(while e₁ e₂)`

**Loop**: `e₁` is evaluated; if it is *true*, then `e₂` is evaluated. The loop repeats, evaluating `e₁` then `e₂`, as long as `e₁` is *true*. When `e₁` becomes 0, `e₂` is not evaluated and the loop ends. In most use cases, `e₂` is built as a `begin` block (see below). 

The value of a complete `while` expression is always 0.


### `(begin e₁ e₂ e₃ …)`

**Block**: evaluate `e₁`, `e₂`, `e₃`, etc. in sequence.

The value of a complete `begin` expression is the value of the last expression in the block.

> **Note**: That's why, in the iterative `gcd` presented a the top of this page, the last line in the outermost `begin` is the expression `n`. That `begin` is the entire body of function, and `n` is the value to be returned.

### `(define f (a₁ a₂ …) e)`

**Function definition**: define a function named `f`, with formal parameters `a₁`, `a₂` etc. The symbols `f`, `a₁`, `a₂` etc. are just names; they are not evaluated. The expression `e` is stored and will be evaluated only when `f` is invoked (applied).
 
Sample usage, defining and using a factorial function named `!` in the REPL:

```lisp
> (define ! (n) (if (< n 2) 1 (* n (! (- n 1)))))
<UserFunction (! n)>
> (! 5)
120
> (! 42)
1405006117752879898543142606244511569936384000000000
```

## Isolated function definitions

**SubPascal** is faithful to Kamin's chapter 1 language, including an important limitation: the `define` statament is handled directly by the REPL, and not by the main evaluator of the interpreter. This means that function definitions may only appear at the top level, as in C. Although Pascal supports nested functions, the main block of a Pascal program is not a function: all functions must be defined outside of that main block. This separation of function definitions from the rest of the program is one of the limitations that are removed in **SubLisp**, Kamin's chapter 2 language. 


## Implementation notes

This is the fourth time I implement Kamin's *chapter 1* language in Python. My priorities this time were:

* Follow more closely the structure and flow of Kamin's Pascal code. A lot of code from the original does not make sense because of the lower level data structures in Pascal — for example, environments built with parallel linked lists instead of dicts. But the most important functions, such as `parse_exp` and `evaluate` are coded similarly. This should make it easier to evolve **SubPascal** into **SubLisp**, **SubSmalltalk** and so on, as I follow Kamin's book.
* Use idiomatic Python, but avoid advanced Python tricks like introspection. Such tricks may eliminate some code at the expense of making it harder to follow. My goal is to talk about interpreters, not advanced Python.
* Provide good test coverage and use TDD. The order of the test cases follows approximately the order of my work implementing the interpreter. Using TDD to build a REPL motivated me to create and publish the [dialogue-tester](https://pypi.org/project/dialogue-tester/) package.
* Provide multiple implementations, with increasing complexity and error handling. See for example the **Calculator** interpreters and the alternative **SubPascal** implementations.

— *Luciano Ramalho, December 2018*
