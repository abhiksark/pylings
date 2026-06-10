# Exceptions

Source: https://docs.python.org/3/tutorial/errors.html#handling-exceptions

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`try` and `except` handle errors without crashing the whole program.

## Extracted reference

8.3. Handling Exceptions

It is possible to write programs that handle selected exceptions. Look at the
following example, which asks the user for input until a valid integer has been
entered, but allows the user to interrupt the program (using Control-C or
whatever the operating system supports); note that a user-generated interruption
is signalled by raising the `KeyboardInterrupt` exception.

```python
>>> while True:
... try:
... x = int(input("Please enter a number: "))
... break
... except ValueError:
... print("Oops! That was no valid number. Try again...")
...

```

The `try` statement works as follows.

-

First, the try clause (the statement(s) between the `try` and
`except` keywords) is executed.
