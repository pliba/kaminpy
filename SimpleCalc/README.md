# SimpleCalc

This is the simplest example of an expression evaluator in the **kaminpy** repository.

**SimpleCalc** is implemented in three functions:

* `tokenize`: to split the input into meaningful tokens for parsing;
* `evaluate`: recursive parser and evaluator;
* `repl`: interactive Read-Eval-Print-Loop.

To highlight the essential recursive algorithm, there is no error checking in `evaluate`.

The Jupyter Notebook has the same code (minus the tests), with simpler type annotations.
