# Exercise: Dataclasses 3
# I AM NOT DONE
#
# Add a default value to the `unit` field of `Measurement` so that
# creating `Measurement(9.8)` works without passing `unit` explicitly.
# The default should be the string "m/s²".
#
# Hint: a default is set by writing `field_name: type = default_value`
# after the required fields.

from dataclasses import dataclass


@dataclass
class Measurement:
    value: float
    unit: str  # Bug: no default — add = "m/s²" here


gravity = Measurement(9.8)
named = Measurement(100.0, "km/h")
