# Exercise: Functions 5
# I AM NOT DONE
#
# Define a function `make_greeting` that takes a `name` parameter and an
# optional `greeting` parameter with a default value of "Hello".
# It should return the string "<greeting>, <name>!".
# Example: make_greeting("Alice") -> "Hello, Alice!"
# Example: make_greeting("Bob", "Hi") -> "Hi, Bob!"

def make_greeting(name, greeting):
    return f"{greeting}, {name}!"
