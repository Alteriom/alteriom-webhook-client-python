# 02_prepare — the version bump pull request

One job: one pull request that sets the version, passes every check, and carries the approved notes for the person to publish.

## Inputs
- Working (this run): `.github/icm/02-release/stages/01_plan/output/release-plan.md`
- Reference (every run): `.github/icm/_shared/release.md`
- Reference (every run): `.github/icm/_shared/build-and-test.md`

Do NOT load: the other pipeline, other runs' output.

## Process
1. Branch `release/X.Y.Z` from current `origin/main`.
2. Set `version` in `pyproject.toml` to `X.Y.Z`; nothing else carries the version ([release.md](../../../_shared/release.md) "The number").
3. In a fresh virtual environment: `pip install -e ".[dev]"`, `pytest tests/ -v`, `python -m build`, and check that `dist/` holds `alteriom_webhook_client-X.Y.Z` wheel and sdist.
4. Open the pull request against `main`, titled `chore: release vX.Y.Z`; the body is the approved notes, the checks' output, and the steps the person takes after the merge.

## Outputs
- release-pr.md → output/ — the pull request link, the diff, the checks' output, and the person's steps: tag `vX.Y.Z` on the merge commit, then publish a GitHub release from that tag with the approved notes.

## Human check
A maintainer reviews the bump with every check green, merges it, and then decides to publish: `gh release create vX.Y.Z --target <merge commit on main> --notes-file <notes>` publishes to PyPI.
