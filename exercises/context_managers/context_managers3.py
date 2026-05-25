# Exercise: Context Managers 3
# I AM NOT DONE
#
# Give the `Timer` class context-manager support so `with Timer() as t:`
# works.
#
# * `__enter__` must return the instance (self).
# * `__exit__` must set `self.finished` to True.
# Both methods take the standard three exception parameters after self.
#
# Hint: `def __exit__(self, exc_type, exc_val, exc_tb):` — set the flag,
# then return None (or False) so exceptions propagate normally.


class Timer:
    def __init__(self):
        self.finished = False

    # Bug: __enter__ and __exit__ are missing — add them.


t = Timer()
with t:
    pass
