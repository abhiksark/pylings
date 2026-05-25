# Exercise: Context Managers 6
# I AM NOT DONE
#
# `contextlib.contextmanager` turns a generator function into a context
# manager.  Write the body of `managed_counter` so it:
#   1. Creates a list `counter = []` before the yield.
#   2. Yields `counter` (the `as` target gets this list).
#   3. Appends the string "finished" to `counter` after the yield.
#
# The `@contextmanager` decorator and the function signature are already
# provided.  Only fill in the body.
#
# Hint: everything before `yield` is __enter__; everything after is __exit__.

from contextlib import contextmanager


@contextmanager
def managed_counter():
    # Bug: body is missing — add counter, yield, then cleanup.
    pass


with managed_counter() as counter:
    counter.append(1)
    counter.append(2)
