# Exercise: Decorators 6
# I AM NOT DONE
#
# Without functools.wraps, a decorator hides the wrapped function's __name__
# and __doc__.  Use @functools.wraps(func) on the inner wrapper to preserve them.
#
# Add the missing import and the @functools.wraps(func) line inside `preserve`.


def preserve(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@preserve
def compute(x, y):
    """Return the sum of x and y."""
    return x + y
