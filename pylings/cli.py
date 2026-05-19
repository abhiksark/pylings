# pylings/cli.py
from __future__ import annotations

import argparse
import sys
from pathlib import Path

__version__ = "0.1.0"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pylings")
    parser.add_argument("--version", action="version", version=f"pylings {__version__}")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Project root containing info.toml (default: cwd).",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("watch", help="Launch the TUI in watch mode (default).")

    p_run = sub.add_parser("run", help="Run a single exercise.")
    p_run.add_argument("name")

    p_hint = sub.add_parser("hint", help="Print the hint for an exercise.")
    p_hint.add_argument("name")

    sub.add_parser("list", help="List exercises with status markers.")

    p_reset = sub.add_parser("reset", help="Restore an exercise from its snapshot.")
    p_reset.add_argument("name")
    p_reset.add_argument("--yes", action="store_true", help="Skip the confirmation prompt.")

    sub.add_parser("verify", help="Run every exercise in order; first failure exits 1.")

    return parser


def _cmd_verify(root: Path) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.runner import run_verify

    manifest = load_manifest(root)
    for ex in manifest.exercises:
        result = run_verify(ex)
        status = "✓" if result.passed else "✗"
        print(f"{status} {ex.name}")
        if not result.passed:
            sys.stderr.write(result.stderr or result.stdout)
            return 1
    return 0


def _cmd_list(root: Path) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.state import load as load_state

    manifest = load_manifest(root)
    state = load_state(root)
    current = state.current or state.next_pending(manifest)
    for ex in manifest.exercises:
        if ex.name in state.completed:
            marker = "✓"
        elif ex.name == current:
            marker = "●"
        else:
            marker = "🔒"
        print(f"  {marker}  {ex.topic}/{ex.name}")
    return 0


def _cmd_hint(root: Path, name: str) -> int:
    from pylings.core.manifest import load as load_manifest

    manifest = load_manifest(root)
    try:
        ex = manifest.by_name(name)
    except KeyError:
        sys.stderr.write(f"pylings: no exercise named {name!r}\n")
        return 1
    print(ex.hint.strip() or "(no hint provided)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    try:
        if args.command == "verify":
            return _cmd_verify(args.root)
        if args.command == "list":
            return _cmd_list(args.root)
        if args.command == "hint":
            return _cmd_hint(args.root, args.name)

        if args.command in (None, "watch"):
            from pylings.app import run_tui  # lazy: Textual is heavy
            return run_tui(args.root)

        # Other subcommands wired in later tasks.
        sys.stderr.write(f"pylings: '{args.command}' not implemented yet\n")
        return 1
    except Exception as e:
        # Manifest errors and other startup failures use exit code 2.
        from pylings.core.manifest import ManifestError
        if isinstance(e, ManifestError):
            sys.stderr.write(f"pylings: {e}\n")
            return 2
        raise
