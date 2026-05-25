# Exercise: Functions 6
# I AM NOT DONE
#
# The function `describe_pet` takes two parameters: `name` and `animal_type`.
# It returns "My <animal_type> is named <name>.".
#
# The call below mixes up the argument order.
# Fix it by using keyword arguments so the result is correct regardless
# of position.
# Store the fixed call result in `description`.

def describe_pet(name, animal_type):
    return f"My {animal_type} is named {name}."

# This call has the arguments in the wrong order:
description = describe_pet("dog", "Buddy")
