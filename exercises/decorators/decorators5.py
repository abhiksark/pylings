# Exercise: Decorators 5
# I AM NOT DONE
#
# The `log_call` decorator should work with functions that take ANY arguments
# (positional and keyword). The wrapper must accept and forward them.
#
# Replace the wrapper signature so it accepts *args and **kwargs, then
# pass them through when calling func.


def log_call(func):
    def wrapper():   # bug: accepts no arguments
        print(f"calling {func.__name__}")
        return func()  # bug: forwards no arguments
    return wrapper


@log_call
def add(a, b):
    return a + b


@log_call
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"
