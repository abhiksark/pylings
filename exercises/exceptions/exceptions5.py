# Exercise: Exceptions 5
# I AM NOT DONE
#
# Complete read_first(items) using a try/finally block.
# - Try to return items[0].
# - If items is empty (IndexError), return None.
# - In the finally clause, append the string "done" to the module-level
#   list `log` — this must happen whether or not an exception occurred.
#
# The finally clause runs ALWAYS, even when an exception is raised or
# a return is executed in the try block.

log = []

def read_first(items):
    try:
        return items[0]
    except IndexError:
        return None
    # TODO: add a finally clause that does log.append("done")
