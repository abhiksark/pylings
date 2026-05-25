# Exercise: Classes 7
# I AM NOT DONE
#
# The `greet` method should call `self.get_name()` to get the name
# and return the greeting string. Replace ??? with the correct call.

class Greeter:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def greet(self):
        return f"Hello, {???}!"


g = Greeter("Alice")
