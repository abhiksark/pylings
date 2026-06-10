# Loops

Source: https://docs.python.org/3/tutorial/controlflow.html#for-statements

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`for` loops iterate over items; `while` loops continue while a condition is true.

## Extracted reference

4.2. `for` Statements

The `for` statement in Python differs a bit from what you may be used
to in C or Pascal. Rather than always iterating over an arithmetic progression
of numbers (like in Pascal), or giving the user the ability to define both the
iteration step and halting condition (as C), Python’s `for` statement
iterates over the items of any sequence (a list or a string), in the order that
they appear in the sequence. For example (no pun intended):

```python
>>> # Measure some strings:
>>> words = ['cat', 'window', 'defenestrate']
>>> for w in words:
... print(w, len(w))
...
cat 3
window 6
defenestrate 12

```

Code that modifies a collection while iterating over that same collection can
be tricky to get right. Instead, it is usually more straight-forward to loop
over a copy of the collection or to create a new collection:

```python
