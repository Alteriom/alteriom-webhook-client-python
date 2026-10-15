# 01-fix — the pipeline

Make it fail, make it pass for the right reason, prove it where CI will.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| [`01_reproduce`](stages/01_reproduce/CONTEXT.md) | reproduce the reported defect | the report | `output/reproduction.md` | A person runs the command or reads its output, confirms it fails for the reported reason, and decides whether a behaviour change is wanted before any fix is written. |
| [`02_fix`](stages/02_fix/CONTEXT.md) | change the cause, not the symptom | 01_reproduce's `reproduction.md` | `output/change.md` | A person reads the diff beside the reproduction: it removes the cause, no verification step was loosened or reordered, and any behaviour change is the one approved. Edit `change.md` if it is wrong; stage 03 reads it. |
| [`03_verify`](stages/03_verify/CONTEXT.md) | checks, pull request | 02_fix's `change.md` | `output/pull-request.md` | A person reads `pull-request.md` and its evidence, then says whether to open it. The reviewer, not the author, merges, once every check on the last commit is green. |
