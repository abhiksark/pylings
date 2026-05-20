# Exercise: Dataclasses 6
# I AM NOT DONE
#
# `@dataclass` generates `__repr__` and `__eq__` automatically.
#
# Fix `Book` so that:
#   * Two Book instances with the same `title` and `pages` compare equal
#     (the generated `__eq__` does this for you).
#   * `repr(book)` contains both the title and page count.
#
# Right now `Book` is a plain class — add `@dataclass` and the two
# typed field declarations `title: str` and `pages: int`.

# Bug: missing @dataclass decorator and field declarations.
class Book:
    pass


novel = Book("Dune", 412)
copy = Book("Dune", 412)
other = Book("Foundation", 255)
