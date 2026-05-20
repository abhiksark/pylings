# Exercise: Context Managers 4
# I AM NOT DONE
#
# `ManagedList` wraps a list and uses `__exit__` to do cleanup.
# When the with-block exits normally, `__exit__` should append the
# string "done" to `self.log`.
#
# The `__enter__` method is already written.  Complete `__exit__` so
# that it appends "done" to `self.log` and returns None.
#
# Hint: `def __exit__(self, exc_type, exc_val, exc_tb): self.log.append("done")`


class ManagedList:
    def __init__(self):
        self.items = []
        self.log = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Bug: cleanup is missing — append "done" to self.log.
        pass


ml = ManagedList()
with ml as resource:
    resource.items.append(1)
    resource.items.append(2)
