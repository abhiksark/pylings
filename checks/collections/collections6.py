assert card.rank == "K", "card rank should be K"
assert card.suit == "spades", "card suit should be spades"
assert upgraded.rank == "A", "upgraded rank should be A"
assert upgraded.suit == "spades", "suit is preserved after _replace"
assert card.suit == upgraded.suit, "_replace does not mutate the original"
print("collections6 ✓")
