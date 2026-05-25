# Exercise: Conditionals 3
# I AM NOT DONE
#
# `elif` lets you chain multiple conditions.  Python tests them in order
# and runs the first branch whose condition is True.
#
# Complete `grade(score)` so it returns:
#   "A" for score >= 90
#   "B" for score >= 80
#   "C" for score >= 70
#   "F" for anything below 70

def grade(score):
    if score >= 90:
        return "A"
    # add the remaining elif / else branches

    return "F"
