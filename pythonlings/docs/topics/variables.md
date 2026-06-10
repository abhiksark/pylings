# Variables

Source: https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Assigning names with `=` lets you keep values for later expressions.

## Extracted reference

3.1. Using Python as a Calculator

Let’s try some simple Python commands. Start the interpreter and wait for the
primary prompt, `>>>`. (It shouldn’t take long.)

3.1.1. Numbers

The interpreter acts as a simple calculator: you can type an expression into it
and it will write the value. Expression syntax is straightforward: the
operators `+`, `-`, `*` and `/` can be used to perform
arithmetic; parentheses (`()`) can be used for grouping.
For example:

```python
>>> 2 + 2
4
>>> 50 - 5*6
20
>>> (50 - 5*6) / 4
5.0
>>> 8 / 5 # division always returns a floating-point number
1.6

```

The integer numbers (e.g. `2`, `4`, `20`) have type `int`,
