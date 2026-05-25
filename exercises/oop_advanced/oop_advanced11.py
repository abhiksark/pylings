# Exercise: Oop Advanced 11
# I AM NOT DONE
#
# Goal: Use a mixin method to turn an object's attributes into a dict.

class DictMixin:
    def to_dict(self):
        return ???

class Product(DictMixin):
    def __init__(self, name, price):
        self.name = name
        self.price = price
