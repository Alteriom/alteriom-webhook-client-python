# 03_publish — the person publishes, the agent confirms

One job: confirm that the release the person published uploaded the right version from the right commit. The agent runs no publishing command.

## Inputs
- Working (this run): `.github/icm/02-release/stages/02_prepare/output/release-pr.md` — or, for a check of an earlier release (route `publish-check`), only the tag `vX.Y.Z` the person names; start at step 2.
- Reference (every run): `.github/icm/_shared/release.md`
- Reference (only when the run failed at the upload): `.github/icm/_shared/gotchas.md`

Do NOT load: the other pipeline, other runs' output, the source tree.

## Process
1. Confirm the tag points at the merge commit on `main` (`git fetch --tags && git branch -r --contains vX.Y.Z` lists `origin/main`) and that `pyproject.toml` there says `X.Y.Z`.
2. Find the `publish.yml` run for the release (`gh run list --workflow publish.yml --limit 3`) and read both jobs. A failure in `test` uploaded nothing. A failure at the upload is read against [gotchas.md](../../../_shared/gotchas.md) "Publishing is tied to names on PyPI's side" before anything is re-run; the person decides the re-run.
3. Check PyPI for `X.Y.Z` (`pip index versions alteriom-webhook-client`), and that a clean environment can `pip install alteriom-webhook-client==X.Y.Z` and import `WebhookReceiver`.

## Outputs
- publication.md → output/ — the tag and its commit; the workflow run with each job's result; the version on PyPI with a link; the install check.

## Human check
A person confirms the version is on PyPI and installs, built from `main`, before it is announced.
