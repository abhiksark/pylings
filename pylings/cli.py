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
    sub.add_parser("topics", help="Launch the TUI on the topic picker.")

    p_run = sub.add_parser("run", help="Run a single exercise.")
    p_run.add_argument("name")

    p_hint = sub.add_parser("hint", help="Print the hint for an exercise.")
    p_hint.add_argument("name")

    p_list = sub.add_parser("list", help="List topics, or one topic's exercises.")
    p_list.add_argument("topic", nargs="?", help="Show exercises of this topic.")

    p_start = sub.add_parser("start", help="Launch the TUI on a topic's track.")
    p_start.add_argument("topic")

    p_reset = sub.add_parser("reset", help="Restore an exercise from its snapshot.")
    p_reset.add_argument("name")
    p_reset.add_argument("--yes", action="store_true", help="Skip the confirmation prompt.")

    p_verify = sub.add_parser(
        "verify", help="Run every exercise, or just one topic's."
    )
    p_verify.add_argument("topic", nargs="?", help="Verify only this topic.")

    return parser


def _snapshot_all(root: Path) -> None:
    """Ensure every exercise has a snapshot in .pylings/originals/."""
    from pylings.core.manifest import load as load_manifest
    from pylings.core.reset import snapshot

    manifest = load_manifest(root)
    for ex in manifest.exercises:
        snapshot(root, ex)


def _resolve_topic(manifest, topic: str):
    """Return the topic name if valid, else write an error and return None."""
    if topic in manifest.topics():
        return topic
    sys.stderr.write(
        f"pylings: no topic named {topic!r}. "
        f"Topics: {', '.join(manifest.topics())}\n"
    )
    return None


def _cmd_verify(root: Path, topic: str | None) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.runner import run_verify

    manifest = load_manifest(root)
    if topic is not None:
        if _resolve_topic(manifest, topic) is None:
            return 2
        exercises = manifest.exercises_in(topic)
    else:
        exercises = manifest.exercises
    for ex in exercises:
        result = run_verify(ex)
        status = "✓" if result.passed else "✗"
        print(f"{status} {ex.name}")
        if not result.passed:
            sys.stderr.write(result.stderr or result.stdout)
            return 1
    return 0


def _cmd_list(root: Path, topic: str | None) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.state import load as load_state, next_pending

    manifest = load_manifest(root)
    state = load_state(root)

    if topic is None:
        for name in manifest.topics():
            exs = manifest.exercises_in(name)
            done = sum(1 for ex in exs if ex.name in state.completed)
            mark = "✓" if done == len(exs) else ("●" if done else " ")
            print(f"  {mark}  {name}  {done}/{len(exs)}")
        return 0

    if _resolve_topic(manifest, topic) is None:
        return 2
    exs = manifest.exercises_in(topic)
    current = next_pending(exs, state.completed)
    for ex in exs:
        if ex.name in state.completed:
            marker = "✓"
        elif ex.name == current:
            marker = "●"
        else:
            marker = "🔒"
        print(f"  {marker}  {ex.name}")
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


def _cmd_run(root: Path, name: str) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.runner import run as run_exercise

    manifest = load_manifest(root)
    try:
        ex = manifest.by_name(name)
    except KeyError:
        sys.stderr.write(f"pylings: no exercise named {name!r}\n")
        return 1

    result = run_exercise(ex)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    if result.timed_out:
        sys.stderr.write(f"pylings: {name} timed out after {result.duration_s:.1f}s\n")
        return 1
    if result.exit_code != 0:
        return 1
    if ex.is_pending():
        sys.stderr.write(
            f"pylings: tests pass but the '# I AM NOT DONE' marker is still in {name}.\n"
        )
        return 1
    return 0


def _cmd_reset(root: Path, name: str, yes: bool) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.reset import ResetError, restore
    from pylings.core.state import load as load_state, save as save_state

    manifest = load_manifest(root)
    try:
        ex = manifest.by_name(name)
    except KeyError:
        sys.stderr.write(f"pylings: no exercise named {name!r}\n")
        return 1

    if not yes:
        sys.stdout.write(f"Reset {name}? (y/N) ")
        sys.stdout.flush()
        if sys.stdin.readline().strip().lower() != "y":
            return 0

    try:
        restore(root, ex)
    except ResetError as e:
        sys.stderr.write(f"pylings: {e}\n")
        return 1

    state = load_state(root)
    state.completed.discard(name)
    save_state(root, state)
    print(f"reset: {name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    try:
        if args.command not in {"hint"}:
            try:
                _snapshot_all(args.root)
            except Exception:
                pass  # snapshot best-effort; real errors surface from subcommands

        if args.command == "verify":
            return _cmd_verify(args.root, args.topic)
        if args.command == "list":
            return _cmd_list(args.root, args.topic)
        if args.command == "hint":
            return _cmd_hint(args.root, args.name)
        if args.command == "run":
            return _cmd_run(args.root, args.name)
        if args.command == "reset":
            return _cmd_reset(args.root, args.name, args.yes)

        if args.command in (None, "watch", "start", "topics"):
            start_topic = getattr(args, "topic", None)
            if start_topic is not None:
                from pylings.core.manifest import load as load_manifest
                if _resolve_topic(load_manifest(args.root), start_topic) is None:
                    return 2
            from pylings.app import run_tui  # lazy: Textual is heavy
            return run_tui(
                args.root,
                start_topic,
                force_picker=args.command == "topics",
            )

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
