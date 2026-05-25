# Exercise: Dataclasses 4
# I AM NOT DONE
#
# The `Basket` dataclass needs a `items` field that defaults to an
# empty list.  You cannot use `items: list = []` directly — Python
# forbids mutable defaults in dataclasses.
#
# Fix the `items` field declaration to use `field(default_factory=list)`
# so each new Basket gets its own independent list.
#
# Hint: import `field` from `dataclasses` and write
#   items: list = field(default_factory=list)

from dataclasses import dataclass


@dataclass
class Basket:
    label: str
    items: list = []  # Bug: mutable default — use field(default_factory=list)


b1 = Basket("fruit")
b2 = Basket("veggies")
b1.items.append("apple")
