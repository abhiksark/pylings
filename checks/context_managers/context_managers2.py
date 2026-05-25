import os

assert f.closed, "f.closed should be True after the with-block exits"

try:
    os.remove(data_path)
except OSError:
    pass

print("context_managers2 ✓")
