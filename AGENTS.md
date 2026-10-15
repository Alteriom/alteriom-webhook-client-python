# alteriom-webhook-client-python

`alteriom-webhook-client` on PyPI: the Python receiving side for deliveries from Alteriom/alteriom-webhook-connector. It verifies the HMAC-SHA256 signature and timestamp, checks size and duplicates, parses the payload into Pydantic v2 models, and offers a FastAPI dependency (MIT, Python 3.10+). It covers only the receiving side; the REST and stream clients are TypeScript only, in Alteriom/webhook-client. What leaves this repository is a reviewed pull request or a version on PyPI.

## Where things live

| Path | What it holds |
|---|---|
| `src/alteriom_webhook_client/` | signature, receiver, models, FastAPI helper — mapped in [architecture.md](.github/icm/_shared/architecture.md) |
| `tests/` | pytest, one file per module |
| `pyproject.toml` | the package, its version, dependencies and extras, the pytest settings |
| `.github/workflows/` | CI (tests on 3.10 to 3.12, build), publish to PyPI on a GitHub release |
| [README.md](README.md) | install and usage, the only user document |
| [`.github/icm/_shared/`](.github/icm/_shared/CONTEXT.md) | what every job below draws on, one file per question |
| [`.github/icm/01-fix/`](.github/icm/01-fix/CLAUDE.md) | fix a defect, or bring a model level with the deliveries |
| [`.github/icm/02-release/`](.github/icm/02-release/CLAUDE.md) | release a version to PyPI; a person publishes the GitHub release |

## Route by what just happened

| Route | If | Go to | Then stop at |
|---|---|---|---|
| triage | an issue arrives and its kind is unclear | read it whole (`gh issue view <n> --comments`) and take the row below that fits | the row chosen, said to the person |
| fix | a defect is reported (issue, failing test, a delivery verified or parsed wrongly) | [01_reproduce](.github/icm/01-fix/stages/01_reproduce/CONTEXT.md) | a person has seen the reproduction fail |
| ci-red | `CI` or `Publish to PyPI` is red | [01_reproduce](.github/icm/01-fix/stages/01_reproduce/CONTEXT.md), with the run log as the report | a person has seen the reproduction fail |
| model-drift | a delivery the service sends fails validation, or Alteriom/webhook-client changed its delivery types | [01_reproduce](.github/icm/01-fix/stages/01_reproduce/CONTEXT.md), with the payload or the change as the report | a person has seen the reproduction fail |
| security | a report may be a vulnerability in the verification | a private report to the maintainers through the repository's Security tab, never a public issue or pull request | the maintainer has the private report |
| release | a version is to be released | [01_plan](.github/icm/02-release/stages/01_plan/CONTEXT.md) | a person approves the version number |
| publish-check | a GitHub release was published and PyPI must be confirmed | [03_publish](.github/icm/02-release/stages/03_publish/CONTEXT.md), from step 2 | a person has seen the version on PyPI |
| next | a stage's output was approved | the next numbered stage of the same job | a person reads that stage's output |
| status | asked for status | scan `.github/icm/*/stages/*/output/` | report what exists |

## Agents connecting remotely

This repository is to be the ICM workspace `alteriom-webhook-client-python` on MemoryRelay. A person creates it from this repository's `main`; the Alteriom hub then delegates to it. Until it exists, and on any clone, an agent needs nothing: this file is the entry, the table above is the route, and the files it links are read directly.

- Once the workspace exists, an agent that is not on a clone reaches the same files over MCP at `https://api.memoryrelay.net/mcp` and starts with `icm_context_build` for the route that fits (`{kind: "route", id: "fix"}`), not with the whole repository.
- Report what you read with `icm_report_reads` when a stage ends, and what the task came to with `icm_report_outcome`.
- Never write through MCP: a change is a branch and a pull request here, read and merged by a person.

## Rules

- Nothing moves to the next stage until a person has read the output of the last one.
- A stage writes to its own `output/`, which is not committed: one run per worktree or branch, and clear that job's `stages/*/output/` when its pull request merges or is abandoned.
- A job reads only its own run's output; moving to another job is a route above, started by the person.
- No agent publishes: a published GitHub release uploads to PyPI, and a person publishes it.
- This repository is public, and the connector is private: no host, secret or connector internals go into a file here.
- `.github/icm/` points at the files that own each fact. When they disagree, the owning file is right: correct `.github/icm/` in the same pull request, and bump its `verified_commit`.
