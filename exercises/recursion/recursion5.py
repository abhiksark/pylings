# Exercise: Recursion 5
# ---------------------
# I AM NOT DONE
#
# Complete `fibonacci(n)` so it returns the nth Fibonacci number using
# recursion.  fibonacci(0) == 0, fibonacci(1) == 1, and for n > 1:
# fibonacci(n) == fibonacci(n - 1) + fibonacci(n - 2).

def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return ???
    return fibonacci(n - 1) + fibonacci(n - 2)
