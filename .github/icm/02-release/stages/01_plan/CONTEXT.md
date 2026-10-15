# 01_plan — choose what ships and its number

One job: a release plan that names the version, justifies its class, and drafts the release notes.

## Inputs
- Working (this run): the changes since the previous release — `git log --oneline v<previous>..origin/main` and `git diff --stat v<previous> origin/main -- src/ pyproject.toml`.
- Reference (every run): `.github/icm/_shared/release.md`
- Reference (every run): `.github/icm/_shared/gotchas.md`

Do NOT load: the other pipeline, other runs' output.

## Process
1. Find the previous tag (`git tag --list 'v*' --sort=-v:refname | head -3`) and what PyPI has (`pip index versions alteriom-webhook-client`).
2. List every merged change and say whether it changes what ships (`src/`, `pyproject.toml` dependencies) or not. Nothing that ships means no release: say so and stop.
3. Classify against [release.md](../../../_shared/release.md) "The number" and say which change decides it. A change to what the receiver accepts is named first.
4. Confirm `main` is green (`gh run list --branch main --workflow ci.yml --limit 3`).
5. Draft the release notes in the shape of `v0.1.0`'s (`gh release view v0.1.0`), with the install line for the new version.

## Outputs
- release-plan.md → output/ — the version and the change that decides its class; what ships; the state of `main`; the drafted notes.

## Human check
A maintainer approves the version number and the notes. The number is permanent once uploaded: PyPI never takes the same version twice.
