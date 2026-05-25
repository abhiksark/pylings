# Exercise: Exceptions 8
# I AM NOT DONE
#
# Complete classify_error(func) so that it calls func() with no arguments
# and returns a string describing what happened:
#   - If no exception: return "ok"
#   - If a ValueError:  return "value error"
#   - If a TypeError:   return "type error"
#   - If any other exception: return "other error"
#
# Use multiple except clauses — each clause catches a different exception type.

def classify_error(func):
    try:
        func()
        return "ok"
    # TODO: add except clauses for ValueError, TypeError, and a catch-all
