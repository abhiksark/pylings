# Exercise: Decorators 2
# I AM NOT DONE
#
# Complete the `shout` decorator: it wraps a function that returns a
# string and makes the wrapper return that string in UPPERCASE.
#
# Hint: str.upper() converts a string to uppercase.


def shout(func):
    def wrapper():
        result = func()
        # return the result, uppercased
        return result
    return wrapper


def greet():
    return "hello"


loud_greet = shout(greet)
