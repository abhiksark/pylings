# Exercise: Context Managers 8
# I AM NOT DONE
#
# Challenge: implement a `Resource` class that tracks acquire/release.
#
# Requirements:
#   * `__init__` sets `self.acquired` to False and `self.release_log` to [].
#   * `__enter__` sets `self.acquired` to True and returns self.
#   * `__exit__` sets `self.acquired` to False and appends the string
#     "released" to `self.release_log`, then returns None.
#
# After that, implement `ManagedPool` using `contextlib.contextmanager`.
# `ManagedPool(resource)` should:
#   1. Call `resource.__enter__()` to acquire it.
#   2. Yield the resource.
#   3. Call `resource.__exit__(None, None, None)` to release it.
#
# Both pieces must work correctly for the checks to pass.

from contextlib import contextmanager


class Resource:
    def __init__(self):
        # Bug: attributes are missing — set acquired and release_log.
        pass

    def __enter__(self):
        # Bug: missing — set acquired, return self.
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Bug: missing — clear acquired, log "released".
        pass


@contextmanager
def ManagedPool(resource):
    # Bug: missing — acquire, yield resource, release.
    pass


r = Resource()
with ManagedPool(r) as res:
    in_block_acquired = res.acquired
