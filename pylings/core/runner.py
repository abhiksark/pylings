# pylings/core/runner.py

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time

from pylings.core.exercise import Exercise
from pylings.core.exercise import RunResult

DEFAULT_TIMEOUT_S = 5.0


def run(exercise: Exercise, timeout_s: float = DEFAULT_TIMEOUT_S) -> RunResult:
    """Run an exercise concatenated with its check file, in a subprocess.

    Never raises.
    """
    start = time.monotonic()
    env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
    }
    exercise_src = exercise.path.read_text(encoding="utf-8")
    combined = (
        exercise_src + "\n\n" + exercise.check_path.read_text(encoding="utf-8")
    )
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    )
    try:
        tmp.write(combined)
        tmp.close()
        try:
            proc = subprocess.run(
                [sys.executable, tmp.name],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_s,
                env=env,
            )
            duration = time.monotonic() - start
            exit_code = proc.returncode
            stdout = proc.stdout
            stderr = proc.stderr
            timed_out = False
        except subprocess.TimeoutExpired as e:
            duration = time.monotonic() - start
            exit_code = -1
            stdout = (
                e.stdout.decode("utf-8", errors="replace")
                if isinstance(e.stdout, bytes)
                else (e.stdout or "")
            )
            stderr = (
                e.stderr.decode("utf-8", errors="replace")
                if isinstance(e.stderr, bytes)
                else (e.stderr or "")
            )
            timed_out = True
        except Exception as e:  # noqa: BLE001 — run() must never raise
            duration = time.monotonic() - start
            exit_code = -1
            stdout = ""
            stderr = f"pylings: failed to run exercise: {e}"
            timed_out = False
    finally:
        os.unlink(tmp.name)

    pending = Exercise.DONE_MARKER in exercise_src
    passed = exit_code == 0 and not timed_out and not pending

    return RunResult(
        passed=passed,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        duration_s=duration,
        timed_out=timed_out,
    )


def run_verify(
    exercise: Exercise, timeout_s: float = DEFAULT_TIMEOUT_S
) -> RunResult:
    """Run an exercise but treat the marker as a no-op (CI / curriculum-author mode)."""
    result = run(exercise, timeout_s=timeout_s)
    # `verify` cares only about exit code; recompute passed without the marker check.
    result.passed = result.exit_code == 0 and not result.timed_out
    return result
