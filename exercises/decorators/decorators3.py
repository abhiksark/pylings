# Exercise: Decorators 3
# I AM NOT DONE
#
# Apply the `stamp` decorator to `get_message` using the `@` syntax
# so that calling get_message() returns "[STAMPED] hello".
#
# The decorator is already written — you only need to add the `@` line
# directly above the `def get_message():` line.


def stamp(func):
    def wrapper():
        return "[STAMPED] " + func()
    return wrapper


def get_message():
    return "hello"
