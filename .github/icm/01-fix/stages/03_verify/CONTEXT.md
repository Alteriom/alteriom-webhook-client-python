# 03_verify — checks, pull request

One job: the pull request a reviewer can merge, with the evidence CI will look for.

## Inputs
- Working (this run): `.github/icm/01-fix/stages/02_fix/output/change.md`
- Reference (every run): `.github/icm/_shared/build-and-test.md`
- Reference (only when the README describes the changed behaviour): `README.md`

Do NOT load: the other pipeline, other runs' output.

## Process
1. Run what CI runs ([build-and-test.md](../../../_shared/build-and-test.md) "What CI runs"): the tests on each Python version you have among 3.10 to 3.12 (at least the oldest), and `python -m build`.
2. Update the `README.md` section that described the old behaviour. Do not change `pyproject.toml`'s version: that is a release.
3. Write the pull request: what was wrong, how you know (the reproduction), what the change does, whether it changes what the receiver accepts; the checks run and their results. Title `fix(<module>): <the outcome>`. Nothing in it names a real secret, host or delivery.
4. After the human check, the agent opens it against `main` (`gh pr create --base main --title "<title>" --body-file <this stage's output/pull-request.md>`). The agent never merges.

## Outputs
- pull-request.md → output/ — the title and body, the checks run with their results, the README change as written.

## Human check
A person reads `pull-request.md` and its evidence, then says whether to open it. The reviewer, not the author, merges, once every check on the last commit is green.
