# Exercise: Type Hints 5
# I AM NOT DONE
#
# Annotate the function `bounding_box` with a fixed-length tuple return type:
#   - parameter `points` should be annotated as `list[tuple[float, float]]`
#   - the return type should be `tuple[float, float, float, float]`
#     (representing min_x, min_y, max_x, max_y)
#
# The signature should read:
#   def bounding_box(points: list[tuple[float, float]]) -> tuple[float, float, float, float]:

def bounding_box(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return (min(xs), min(ys), max(xs), max(ys))
