# Dictionaries

Source: https://docs.python.org/3/tutorial/datastructures.html#dictionaries

This local reference is generated from the official Python documentation and trimmed for pylings.

Dictionaries map keys to values and are the standard way to represent lookup tables.

## Extracted reference

5.5. Dictionaries

Another useful data type built into Python is the dictionary (see
Mapping Types — dict). Dictionaries are sometimes found in other languages as
“associative memories” or “associative arrays”. Unlike sequences, which are
indexed by a range of numbers, dictionaries are indexed by keys, which can be
any immutable type; strings and numbers can always be keys. Tuples can be used
as keys if they contain only strings, numbers, or tuples; if a tuple contains
any mutable object either directly or indirectly, it cannot be used as a key.
You can’t use lists as keys, since lists can be modified in place using index
assignments, slice assignments, or methods like `append()` and
`extend()`.

It is best to think of a dictionary as a set of key: value pairs,
with the requirement that the keys are unique (within one dictionary). A pair of
braces creates an empty dictionary: `{}`. Placing a comma-separated list of
key:value pairs within the braces adds initial key:value pairs to the
dictionary; this is also the way dictionaries are written on output.

The main operations on a dictionary are storing a value with some key and
extracting the value given the key. It is also possible to delete a key:value
pair with `del`. If you store using a key that is already in use, the old
value associated with that key is forgotten.

Extracting a value for a non-existent key by subscripting (`d[key]`) raises a
`KeyError`. To avoid getting this error when trying to access a possibly
