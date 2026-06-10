# pythonlings/core/runner.py

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time

from pythonlings.core.exercise import Exercise
from pythonlings.core.exercise import RunResult

DEFAULT_TIMEOUT_S = 5.0


def run(exercise: Exercise, timeout_s: float = DEFAULT_TIMEOUT_S) -> RunResult:
    """Run an exercise concatenated with its check file, in a subprocess.

    Never raises.
    """
    start = time.monotonic()
    exercise_path = exercise.path.resolve()
    check_path = exercise.check_path.resolve()
    env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
    }
    exercise_src = exercise_path.read_text(encoding="utf-8")
    runner_src = (
        "import sys\n"
        "from pathlib import Path\n"
        f"exercise_path = Path({str(exercise_path)!r})\n"
        f"check_path = Path({str(check_path)!r})\n"
        "sys.path.insert(0, str(Path.cwd()))\n"
        "namespace = {\n"
        "    '__name__': '__main__',\n"
        "    '__file__': str(exercise_path),\n"
        "    '__package__': None,\n"
        "}\n"
        "exercise_src = exercise_path.read_text(encoding='utf-8')\n"
        "check_src = check_path.read_text(encoding='utf-8')\n"
        "exec(compile(exercise_src, str(exercise_path), 'exec'), namespace)\n"
        "namespace['__file__'] = str(check_path)\n"
        "exec(compile(check_src, str(check_path), 'exec'), namespace)\n"
    )
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    )
    try:
        tmp.write(runner_src)
        tmp.close()
        try:
            cwd = (exercise.root or exercise_path.parent).resolve()
            proc = subprocess.run(
                [sys.executable, tmp.name],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_s,
                env=env,
                cwd=cwd,
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
            stderr = f"pythonlings: failed to run exercise: {e}"
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
