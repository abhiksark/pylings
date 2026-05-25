from pylings.cli import main


def test_dry_run_alias_runs_one_exercise() -> None:
    code = main(["--root", "tests/fixtures/passing_curriculum", "dry-run", "passing1"])

    assert code == 0
