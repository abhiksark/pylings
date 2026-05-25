import os

with open(dst_path) as _f:
    _result = _f.read()

assert _result == "HELLO WORLD\nPYTHON IS FUN\nFILE IO ROCKS\n", (
    f"dst_path should contain uppercased text, got {_result!r}"
)

for _p in (src_path, dst_path):
    try:
        os.remove(_p)
    except OSError:
        pass

print("file_io10 ✓")
