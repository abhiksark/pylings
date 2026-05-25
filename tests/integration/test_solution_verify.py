from pathlib import Path

from pylings.core.manifest import load
from pylings.core.runner import run_verify
from pylings.core.solutions import solution_exercise


def test_every_reference_solution_passes() -> None:
    root = Path(__file__).resolve().parents[2]
    manifest = load(root)
    failures: list[str] = []

    for exercise in manifest.exercises:
        result = run_verify(solution_exercise(root, exercise))
        if not result.passed:
            failures.append(f"{exercise.name}: {result.stderr or result.stdout}")

    assert failures == []
