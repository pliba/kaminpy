# kaminpy

This repository contains Python implementations of the interpreters described
in Samuel Kamin's excellent PLIBA [1] book.

[1] Samuel Kamin, "Programming Languages, An Interpreter-Based Approach",
      Addison-Wesley, Reading, MA, 1990. ISBN 0-201-06824-9.

## Python examples

### Introductory

Examples designed to make it easier to understand the essentials of an interpreter.

* [Calculator](https://github.com/pliba/kaminpy/tree/master/Calculator): arithmetic expressions calculator.

* [CalcWithVars](https://github.com/pliba/kaminpy/tree/master/CalcWithVars): arithmetic expressions calculator with veriables.

### SubPascal

Kamin's *"chapter 1 language"*, minimal yet Turing-complete, inspired by Pascal with s-expression syntax. **SubPascal** is our name for it.

* [SubPascalWithoutFunc](https://github.com/pliba/kaminpy/tree/master/SubPascalWithoutFunc): SubPascal without function definitions.

* [SubPascalHappyPaths](https://github.com/pliba/kaminpy/tree/master/SubPascalHappyPaths): "complete" SubPascal language, with function definitions but almost no error handling and limited REPL.

* [SubPascal](https://github.com/pliba/kaminpy/tree/master/SubPascal): complete SubPascal with better error handling, multi-line REPL and source file execution.



## Source material

PLIBA book errata and source code in Pascal and C:

http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/lang/lisp/impl/kamin/0.html
