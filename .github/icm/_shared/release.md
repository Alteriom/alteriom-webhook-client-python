---
verified_at: 2026-10-15
verified_commit: 337bb90fc61fd822113654f550d491de4e76aa38
---

# Releasing — from a version bump to PyPI

## The number

Semantic versioning on `pyproject.toml:7`, the only place the version lives. A fix is a patch; a new optional field, model or keyword argument is a minor; a removed or renamed public name (`src/alteriom_webhook_client/__init__.py` `__all__`), a field made required, or a check that rejects what it used to accept is a breaking change, said first in the release notes; while the version is below 1.0, the person decides at the plan whether it is a minor or 1.0. There is no changelog file: the GitHub release notes are the record (`v0.1.0` is the one so far).

## What publishes

`publish.yml` runs when a GitHub release is published (`.github/workflows/publish.yml:5`): the tests on 3.12, `python -m build`, then `pypa/gh-action-pypi-publish` with PyPI trusted publishing (OIDC, `id-token: write`) in the `pypi` environment (`.github/workflows/publish.yml:25`). There is no token secret. Publishing the GitHub release is the publish decision, and a person makes it, after the version bump has merged to `main`, on a `vX.Y.Z` tag at that merge.

Nothing checks that the tag matches `pyproject.toml`: the version uploaded is the one in `pyproject.toml` at the tagged commit, and PyPI refuses a version it already has, so a release without a bump fails at the upload step.

## Afterwards

PyPI: `pip index versions alteriom-webhook-client` or the project page. A run that failed before the upload published nothing; once a version is uploaded it is there for good, because PyPI never accepts the same version twice. A broken upload is followed by a new patch version, never by a re-tag. The first release needed three runs while the workflow moved to trusted publishing (`git log --oneline -- .github/workflows/publish.yml`).
