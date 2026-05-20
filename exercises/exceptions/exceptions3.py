# Exercise: Exceptions 3
# I AM NOT DONE
#
# Complete describe_error(s) so that it tries to convert `s` to a float,
# returning the float on success.  On failure it should return the string
# representation of the exception message (i.e. str(e)), NOT a fixed string.
#
# Capture the exception object with `as`:
#   except ValueError as e:
#       return str(e)

def describe_error(s):
    return float(s)
