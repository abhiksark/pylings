# Tuples

Source: https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences

This local reference is generated from the official Python documentation and trimmed for pylings.

Tuples group ordered values and are commonly unpacked into multiple names.

## Extracted reference

5.3. Tuples and Sequences

We saw that lists and strings have many common properties, such as indexing and
slicing operations. They are two examples of sequence data types (see
Sequence Types — list, tuple, range). Since Python is an evolving language, other sequence data
types may be added. There is also another standard sequence data type: the
tuple.

A tuple consists of a number of values separated by commas, for instance:

```python
>>> t = 12345, 54321, 'hello!'
>>> t[0]
12345
>>> t
(12345, 54321, 'hello!')
>>> # Tuples may be nested:
>>> u = t, (1, 2, 3, 4, 5)
>>> u
((12345, 54321, 'hello!'), (1, 2, 3, 4, 5))
>>> # Tuples are immutable:
>>> t[0] = 88888
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> # but they can contain mutable objects:
