# Release Checklist

Pylings follows Semantic Versioning. Use full `MAJOR.MINOR.PATCH` versions in
package metadata and annotated git tags such as `v0.1.0`.

## Package Name

The PyPI name `pylings` is already owned by another project. This repository's
distribution name is `python-learnings`; installing it provides the `pylings`
console command. Do not document `pip install pylings` for this project unless
the package name is transferred.

## Pre-Release Verification

Run these checks from a clean working tree before tagging:

```bash
python -m pytest -q
pylings --root tests/fixtures/passing_curriculum verify
python -m build
python -m pip install --force-reinstall dist/python_learnings-*.whl
pylings --version
tmp=$(mktemp -d /tmp/pylings-release.XXXXXX)
pylings init --path "$tmp"
pylings --root "$tmp" list
pylings --root "$tmp" solution variables1
pylings --root "$tmp" reset variables1 --yes
```

Expected release version for `v0.1.0`:

```text
pylings 0.1.0
```

## Tag And Publish

1. Commit the release changes.
2. Create an annotated tag, for example `git tag -a v0.1.0 -m "Release v0.1.0"`.
3. Push the branch and tag.
4. Create a GitHub Release from the tag.
5. The `publish` workflow builds the package, checks that the release tag
   matches `pyproject.toml`, smoke-tests the installed wheel, then publishes to
   PyPI through trusted publishing.
