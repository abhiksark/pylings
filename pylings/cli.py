import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pylings")
    parser.add_argument("--version", action="version", version="pylings 0.1.0")
    parser.parse_args(argv if argv is not None else sys.argv[1:])
    print("pylings: not implemented yet", file=sys.stderr)
    return 0
