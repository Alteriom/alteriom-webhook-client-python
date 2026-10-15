# 01_reproduce — reproduce the reported defect

One job: turn the report into a pytest case that fails on demand, for the reason reported.

## Inputs
- Working (this run): the report — read whole with what it links: an issue (`gh issue view <n> --comments`), a red run (`gh run view <run-id> --log-failed`), a delivery the receiver rejected or parsed wrongly, or a change to the delivery types in Alteriom/webhook-client.
- Reference (every run): `.github/icm/_shared/architecture.md`
- Reference (every run): `.github/icm/_shared/build-and-test.md`
- Reference (every run): `.github/icm/_shared/gotchas.md`

Do NOT load: the other pipeline, `.github/icm/_shared/release.md`, other runs' output.

## Process
1. If the report could be a vulnerability in the verification (a signature, timestamp or size check that can be bypassed), stop before writing anything: this pipeline ends in a public pull request, and a private report through the repository's Security tab is the route.
2. Restate the report as observed versus expected: the input (a delivery with every secret, id and repository name replaced by test values), the step of the pipeline that answered, and what it should have done.
3. Find the step with [architecture.md](../../../_shared/architecture.md) and name the suspected cause as `path:line`. For `model-drift`, name the field and the value the model refuses, and where the TypeScript types or the supplied delivery show it.
4. In a virtual environment with `pip install -e ".[dev]"`, write the failing test in the file [build-and-test.md](../../../_shared/build-and-test.md) "Where a test belongs" names, signing deliveries with `sign_payload` and a current timestamp as the existing tests do.
5. Run it (`pytest tests/<file> -v`) and keep the failing output. If it passes, the reproduction or the report is wrong: say which, and stop.
6. Say whether the fix will change what the receiver accepts or a public name ([gotchas.md](../../../_shared/gotchas.md) "Deliveries without an aggregate count as duplicates" is one already open).

## Outputs
- reproduction.md → output/ — the restated report; the suspected cause (`path:line`); the test and command; the failing output; whether the fix is a behaviour change.

## Human check
A person runs the command or reads its output, confirms it fails for the reported reason, and decides whether a behaviour change is wanted before any fix is written.
