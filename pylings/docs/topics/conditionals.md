# Conditionals

Source: https://docs.python.org/3/tutorial/controlflow.html#if-statements

This local reference is generated from the official Python documentation and trimmed for pylings.

`if`, `elif`, and `else` choose which block runs based on boolean conditions.

## Extracted reference

4.1. `if` Statements

Perhaps the most well-known statement type is the `if` statement. For
example:

```python
>>> x = int(input("Please enter an integer: "))
Please enter an integer: 42
>>> if x < 0:
... x = 0
... print('Negative changed to zero')
... elif x == 0:
... print('Zero')
... elif x == 1:
... print('Single')
... else:
... print('More')
...
More

```

There can be zero or more `elif` parts, and the `else` part is
optional. The keyword ‘`elif`’ is short for ‘else if’, and is useful
to avoid excessive indentation. An `if` … `elif` …
`elif` … sequence is a substitute for the `switch` or
