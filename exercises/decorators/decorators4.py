# Exercise: Decorators 4
# I AM NOT DONE
#
# The `double_result` decorator should wrap `func`, call it, and return
# the return value multiplied by 2.
#
# Right now the wrapper does NOT return anything (returns None).
# Fix the wrapper so it captures and returns double the wrapped function's result.


def double_result(func):
    def wrapper():
        func()   # bug: the return value is thrown away
    return wrapper


@double_result
def get_five():
    return 5


@double_result
def get_ten():
    return 10
