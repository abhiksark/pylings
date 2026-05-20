# Exercise: Type Hints 3
# I AM NOT DONE
#
# Annotate the function `total` to use parameterized generic types:
#   - parameter `scores` should be annotated as `list[int]`
#   - parameter `labels` should be annotated as `dict[str, int]`
#   - the return type should be annotated as `int`
#
# The signature should read:
#   def total(scores: list[int], labels: dict[str, int]) -> int:

def total(scores, labels):
    return sum(scores) + sum(labels.values())
