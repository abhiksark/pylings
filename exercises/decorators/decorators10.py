# Exercise: Decorators 10
# I AM NOT DONE
#
# Implement the `memoize` decorator: it caches the result of each unique
# set of arguments so that the wrapped function is called at most once
# per distinct input.
#
# The cache should be stored in a dict as an attribute: wrapper.cache
# Use the tuple of positional args as the cache key (assume no kwargs).
#
# Fill in the wrapper body — right now it ignores the cache entirely.

import functools


def memoize(func):
    @functools.wraps(func)
    def wrapper(*args):
        # bug: always calls func, never checks or updates the cache
        return func(*args)
    wrapper.cache = {}
    return wrapper


call_count = 0


@memoize
def slow_square(n):
    global call_count
    call_count += 1
    return n * n
