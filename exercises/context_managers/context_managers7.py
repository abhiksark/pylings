# Exercise: Context Managers 7
# I AM NOT DONE
#
# `__exit__` can suppress exceptions by returning True.  Complete
# `SilentZeroDivision` so that any ZeroDivisionError raised inside
# the with-block is silently swallowed (execution continues after
# the with-block as if no exception occurred).
#
# * If `exc_type` is `ZeroDivisionError`, return True (suppress it).
# * For every other exception (or no exception), return None (propagate).
#
# Hint: `if exc_type is ZeroDivisionError: return True`


class SilentZeroDivision:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Bug: always returns None, so ZeroDivisionError is not suppressed.
        return None


result = "not set"
with SilentZeroDivision():
    result = 1 / 0        # should be suppressed
    result = "unreachable"

# If suppression works, `result` stays "not set" because the exception
# aborts the rest of the block body before the second assignment.
