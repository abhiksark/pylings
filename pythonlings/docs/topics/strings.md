# Strings

Source: https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Strings are immutable text sequences with indexing, slicing, and many useful methods.

## Extracted reference

Text Sequence Type — `str`

Textual data in Python is handled with `str` objects, or strings.
Strings are immutable
sequences of Unicode code points. String literals are
written in a variety of ways:

-

Single quotes: `'allows embedded "double" quotes'`

-

Double quotes: `"allows embedded 'single' quotes"`

-

Triple quoted: `'''Three single quotes'''`, `"""Three double quotes"""`

Triple quoted strings may span multiple lines - all associated whitespace will
be included in the string literal.

String literals that are part of a single expression and have only whitespace
between them will be implicitly converted to a single string literal. That
is, `("spam " "eggs") == "spam eggs"`.
