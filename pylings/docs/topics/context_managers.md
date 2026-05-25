# Context Managers

Source: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement

This local reference is generated from the official Python documentation and trimmed for pylings.

Context managers run setup and cleanup around a block using `with`.

## Extracted reference

8.5. The `with` statement

The `with` statement is used to wrap the execution of a block with
methods defined by a context manager (see section With Statement Context Managers).
This allows common `try`…`except`…`finally`
usage patterns to be encapsulated for convenient reuse.

```python

with_stmt: "with" ( "(" with_stmt_contents ","? ")" | with_stmt_contents ) ":" suite
with_stmt_contents: with_item ("," with_item)*
with_item: expression ["as" target]

```

The execution of the `with` statement with one “item” proceeds as follows:

-

The context expression (the expression given in the
`with_item`) is evaluated to obtain a context manager.

-

The context manager’s `__enter__()` is loaded for later use.
