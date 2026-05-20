# Exercise: Exceptions 4
# I AM NOT DONE
#
# Complete load_value(data, key) so it uses a try/except/else block:
#   - try to retrieve data[key]
#   - if a KeyError occurs, return the string "missing"
#   - in the else clause (runs only when no exception occurred),
#     return the value doubled (value * 2)
#
# The else clause of a try block runs when NO exception was raised.

def load_value(data, key):
    try:
        value = data[key]
    except KeyError:
        return "missing"
    # TODO: add an else clause here that returns value * 2
