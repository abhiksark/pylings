# Classes

Source: https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Classes combine data and behavior into reusable types.

## Extracted reference

9.3. A First Look at Classes

Classes introduce a little bit of new syntax, three new object types, and some
new semantics.

9.3.1. Class Definition Syntax

The simplest form of class definition looks like this:

```python
class ClassName:
<statement-1>
.
.
.
<statement-N>

```

Class definitions, like function definitions (`def` statements) must be
executed before they have any effect. (You could conceivably place a class
definition in a branch of an `if` statement, or inside a function.)

In practice, the statements inside a class definition will usually be function
definitions, but other statements are allowed, and sometimes useful — we’ll
come back to this later. The function definitions inside a class normally have
