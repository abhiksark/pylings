# Generators

Source: https://docs.python.org/3/tutorial/classes.html#generators

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Generators produce values lazily with `yield` instead of returning a whole collection.

## Extracted reference

9.9. Generators

Generators are a simple and powerful tool for creating iterators. They
are written like regular functions but use the `yield` statement
whenever they want to return data. Each time `next()` is called on it, the
generator resumes where it left off (it remembers all the data values and which
statement was last executed). An example shows that generators can be trivially
easy to create:

```python
def reverse(data):
for index in range(len(data)-1, -1, -1):
yield data[index]

```

```python
>>> for char in reverse('golf'):
... print(char)
...
f
l
o
g

```
