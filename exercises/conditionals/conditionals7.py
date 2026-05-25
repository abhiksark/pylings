# Exercise: Conditionals 7
# I AM NOT DONE
#
# Nested `if` statements let you check a second condition only after
# a first condition has already passed.
#
# Complete `ticket_price(age, is_member)` using nested if/else:
#   - Under 5 years old  => free (0)
#   - 5 or older AND a member => 8
#   - 5 or older AND NOT a member => 12

def ticket_price(age, is_member):
    if age < 5:
        return 0
    else:
        if ???:
            return 8
        ???
