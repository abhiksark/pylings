# Exercise: Oop Advanced 2
# I AM NOT DONE
#
# Goal: Use super() so Employee initializes the Person name.

class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):
    def __init__(self, name, role):
        ???
        self.role = role
