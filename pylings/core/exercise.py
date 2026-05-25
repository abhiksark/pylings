# pylings/core/exercise.py

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Exercise:
    name: str
    path: Path
    check_path: Path
    topic: str
    hint: str
    docs: str = ""
    root: Path | None = None
    rel_path: Path | None = None
    check_rel_path: Path | None = None

    DONE_MARKER = "# I AM NOT DONE"

    def is_pending(self) -> bool:
        return self.DONE_MARKER in self.path.read_text(encoding="utf-8")


@dataclass
class RunResult:
    passed: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_s: float
    timed_out: bool
