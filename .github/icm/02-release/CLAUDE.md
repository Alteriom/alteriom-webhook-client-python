# 02-release — release a version

One run is one version of `alteriom-webhook-client`, from the merged changes to the same number on PyPI. One release so far (`v0.1.0`), and it took three runs of `publish.yml` while publishing moved to trusted publishing, which is why the steps are written down.

A published GitHub release uploads to PyPI, so publishing it is the person's act, after the version bump has merged. The agent plans, prepares the bump, drafts the notes, and confirms the result. It never creates a tag or a release, and never uploads.

Stages, in order; inputs, outputs and checks for each are in [CONTEXT.md](CONTEXT.md):

1. [Plan](stages/01_plan/CONTEXT.md) — what ships, and which number.
2. [Prepare](stages/02_prepare/CONTEXT.md) — the version bump pull request and the draft notes.
3. [Publish](stages/03_publish/CONTEXT.md) — the person publishes the release; the agent confirms PyPI.
