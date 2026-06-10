# File I/O

Source: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`open` and `with` are the usual tools for reading and writing files safely.

## Extracted reference

7.2. Reading and Writing Files

`open()` returns a file object, and is most commonly used with
two positional arguments and one keyword argument:
`open(filename, mode, encoding=None)`

```python
>>> f = open('workfile', 'w', encoding="utf-8")

```

The first argument is a string containing the filename. The second argument is
another string containing a few characters describing the way in which the file
will be used. mode can be `'r'` when the file will only be read, `'w'`
for only writing (an existing file with the same name will be erased), and
`'a'` opens the file for appending; any data written to the file is
automatically added to the end. `'r+'` opens the file for both reading and
writing. The mode argument is optional; `'r'` will be assumed if it’s
omitted.

Normally, files are opened in text mode, that means, you read and write
strings from and to the file, which are encoded in a specific encoding.
If encoding is not specified, the default is platform dependent
(see `open()`).
Because UTF-8 is the modern de-facto standard, `encoding="utf-8"` is
recommended unless you know that you need to use a different encoding.
