from pathlib import Path

import tomllib


def test_every_exercise_has_solution_file() -> None:
    root = Path(__file__).resolve().parents[2]
    data = tomllib.loads((root / "info.toml").read_text(encoding="utf-8"))
    missing = [
        entry["name"]
        for entry in data["exercises"]
        if not (root / "solutions" / f"{entry['name']}.py").exists()
    ]

    assert missing == []
