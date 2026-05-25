# Exercise: Collections 6
# -----------------------
# I AM NOT DONE
#
# Named-tuple fields can be accessed by name OR by index, just like a
# regular tuple.  They also support `._replace()` to build a modified copy.
#
# A `Card` namedtuple with fields `rank` and `suit` is defined for you.
# 1. Create `card` — the King of Spades (rank="K", suit="spades").
# 2. Create `upgraded` by replacing the rank of `card` with "A"
#    using `card._replace(...)`.

from collections import namedtuple

Card = namedtuple("Card", ["rank", "suit"])

card = ???
upgraded = ???
