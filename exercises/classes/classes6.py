# Exercise: Classes 6
# I AM NOT DONE
#
# Give the `speed` parameter in Car.__init__ a default value of 0,
# so that `Car("Tesla")` works without passing a speed.
# Right now `speed` has no default, so the call below raises a TypeError.

class Car:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed


slow = Car("Tesla")
fast = Car("Ferrari", 200)
