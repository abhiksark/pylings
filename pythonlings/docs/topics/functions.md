# Functions

Source: https://docs.python.org/3/tutorial/controlflow.html#defining-functions

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`def` creates reusable behavior with parameters, return values, and optional defaults.

## Extracted reference

4.8. Defining Functions

We can create a function that writes the Fibonacci series to an arbitrary
boundary:

```python
>>> def fib(n): # write Fibonacci series less than n
... """Print a Fibonacci series less than n."""
... a, b = 0, 1
... while a < n:
... print(a, end=' ')
... a, b = b, a+b
... print()
...
>>> # Now call the function we just defined:
>>> fib(2000)
0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597

```

The keyword `def` introduces a function definition. It must be
followed by the function name and the parenthesized list of formal parameters.
The statements that form the body of the function start at the next line, and
must be indented.

The first statement of the function body can optionally be a string literal;
