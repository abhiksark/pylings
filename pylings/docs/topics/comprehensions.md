# Comprehensions

Source: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions

This local reference is generated from the official Python documentation and trimmed for pylings.

Comprehensions build new collections by combining an expression with one or more loops.

## Extracted reference

5.1.3. List Comprehensions

List comprehensions provide a concise way to create lists.
Common applications are to make new lists where each element is the result of
some operations applied to each member of another sequence or iterable, or to
create a subsequence of those elements that satisfy a certain condition.

For example, assume we want to create a list of squares, like:

```python
>>> squares = []
>>> for x in range(10):
... squares.append(x**2)
...
>>> squares
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

```

Note that this creates (or overwrites) a variable named `x` that still exists
after the loop completes. We can calculate the list of squares without any
side effects using:

```python
squares = list(map(lambda x: x**2, range(10)))
