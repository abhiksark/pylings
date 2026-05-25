# Exercise: Lists 9
# I AM NOT DONE
#
# A matrix is stored as a list of rows (a list of lists).
# Fix the two ??? expressions to extract the correct cells:
#   `center`      — the element at row 1, column 1  (should be 5)
#   `bottom_right` — the element at row 2, column 2  (should be 9)
# Then set `matrix[0][2]` to 99.

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

center       = matrix[???][???]
bottom_right = matrix[???][???]

matrix[0][2] = 99
