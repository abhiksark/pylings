# Exercise: Decorators 7
# I AM NOT DONE
#
# The `count_calls` decorator should track how many times the decorated
# function has been called. The count is stored as an attribute on the
# wrapper: wrapper.call_count, starting at 0 and incrementing on each call.
#
# Right now the count is never updated. Fix the wrapper to increment
# wrapper.call_count before forwarding the call.

import functools


def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # bug: call_count is never incremented
        return func(*args, **kwargs)
    wrapper.call_count = 0
    return wrapper


@count_calls
def add(a, b):
    return a + b
