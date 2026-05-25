# Exercise: Type Hints 6
# I AM NOT DONE
#
# Create a type alias `Vector` that equals `list[float]`, then annotate
# the function `scale`:
#   - parameter `v` should be annotated as `Vector`
#   - parameter `factor` should be annotated as `float`
#   - the return type should be `Vector`
#
# Write:
#   Vector = list[float]
#
#   def scale(v: Vector, factor: float) -> Vector:

def scale(v, factor):
    return [x * factor for x in v]
