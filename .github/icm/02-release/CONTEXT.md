# 02-release — the pipeline

Choose the number, bump it in one pull request, let a person publish the release, and confirm PyPI has it.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| [`01_plan`](stages/01_plan/CONTEXT.md) | choose what ships and its number | the changes since the previous release | `output/release-plan.md` | A maintainer approves the version number and the notes. The number is permanent once uploaded: PyPI never takes the same version twice. |
| [`02_prepare`](stages/02_prepare/CONTEXT.md) | the version bump pull request | 01_plan's `release-plan.md` | `output/release-pr.md` | A maintainer reviews the bump with every check green, merges it, and then decides to publish: `gh release create vX.Y.Z --target <merge commit on main> --notes-file <notes>` publishes to PyPI. |
| [`03_publish`](stages/03_publish/CONTEXT.md) | the person publishes, the agent confirms | 02_prepare's `release-pr.md` | `output/publication.md` | A person confirms the version is on PyPI and installs, built from `main`, before it is announced. |
