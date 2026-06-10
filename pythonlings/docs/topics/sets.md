# Sets

Source: https://docs.python.org/3/tutorial/datastructures.html#sets

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Sets store unique values and support membership tests and set operations.

## Extracted reference

5.4. Sets

Python also includes a data type for sets. A set is
an unordered collection with no duplicate elements. Basic uses include
membership testing and eliminating duplicate entries. Set objects also
support mathematical operations like union, intersection, difference, and
symmetric difference.

Curly braces or the `set()` function can be used to create sets. Note: to
create an empty set you have to use `set()`, not `{}`; the latter creates an
empty dictionary, a data structure that we discuss in the next section.

Because sets are unordered, iterating over them or printing them can
produce the elements in a different order than you expect.

Here is a brief demonstration:

```python
>>> basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
>>> print(basket) # show that duplicates have been removed
{'orange', 'banana', 'pear', 'apple'}
>>> 'orange' in basket # fast membership testing
True
>>> 'crabgrass' in basket
False
