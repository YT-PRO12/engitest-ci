# Package release acceptance checklist

EngiTest CI builds and tests a numerical Python package. Its workflow does not publish a production release.

1. Install locked or documented dev dependencies in a clean environment.
2. Run lint and `python -m pytest` including coverage thresholds.
3. Build the wheel and source distribution with `python -m build`.
4. Run `python scripts/smoke_wheel.py` to check an isolated wheel installation.
5. Verify numerical reference outputs and import availability from the installed wheel.
6. Record the source commit SHA, package hashes, CI run link, and failures or skips.

A Jenkinsfile is configuration, not proof of an executed Jenkins job. Test artifacts and a successful source-tree import alone do not establish package distribution correctness.

See [README](../README.md) and [VERIFICATION](../VERIFICATION.md).
