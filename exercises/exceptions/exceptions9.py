# Exercise: Exceptions 9
# I AM NOT DONE
#
# Define a custom exception class called `InsufficientFundsError` that
# inherits from Exception.
#
# Then complete withdraw(balance, amount) so that:
# - If amount > balance, raise InsufficientFundsError with the message:
#   "cannot withdraw <amount> from balance of <balance>"
# - Otherwise return balance - amount.
#
# A custom exception class looks like:
#   class MyError(Exception):
#       pass

# TODO: define InsufficientFundsError here

def withdraw(balance, amount):
    # TODO: raise InsufficientFundsError when amount > balance
    return balance - amount
