# Exercise: Exceptions 10
# I AM NOT DONE
#
# Complete validate_username(name) which enforces three rules:
#   1. The name must be a str; if not, raise TypeError("username must be a str").
#   2. The name must be between 3 and 20 characters (inclusive); if not,
#      raise ValueError("username must be 3–20 characters").
#   3. The name must contain only letters and digits (name.isalnum()); if not,
#      raise ValueError("username must be alphanumeric").
#
# On success, return name.lower().
#
# Check the rules in the order listed above.

def validate_username(name):
    # TODO: check type (raise TypeError if not str)
    # TODO: check length (raise ValueError if out of 3–20 range)
    # TODO: check alphanumeric (raise ValueError if not .isalnum())
    return name.lower()
