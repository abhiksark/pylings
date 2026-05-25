# Exercise: Itertools 4
# I AM NOT DONE
#
# Goal: Use groupby to group sorted rows by category.

from itertools import groupby

rows = [("fruit", "apple"), ("fruit", "pear"), ("veg", "carrot")]
grouped = {
    category: [name for _, name in group]
    for category, group in groupby(rows, key=??? )
}
