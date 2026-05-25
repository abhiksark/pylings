# Exercise: Testing 9
# I AM NOT DONE
#
# A *fixture* is a helper that builds the test data your tests need.
# In plain Python you write a setup function and call it at the top of
# each test that needs it:
#
#   def make_shopping_cart():
#       return {"items": [], "discount": 0}
#
#   def test_add_item():
#       cart = make_shopping_cart()
#       ...
#
# `make_user` below is the fixture. Complete `test_user_greeting` so it:
#   1. Calls `make_user()` to get a fresh user dict.
#   2. Asserts that `greet(user)` returns "Hello, Alice!"

def make_user():
    return {"name": "Alice", "age": 30}


def greet(user):
    return f"Hello, {user['name']}!"


def test_user_greeting():
    # 1. call make_user() to get the fixture
    # 2. assert greet(user) == "Hello, Alice!"
    pass
