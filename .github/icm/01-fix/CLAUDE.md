# 01-fix — fix a defect

One run is one defect in the signature, the receiver pipeline, the models or the FastAPI helper, or a model that has fallen behind the deliveries (route `model-drift`): reproduced, fixed at its cause, and proposed as a pull request with the evidence. The history so far is the package itself and the fixes that made its publishing work (`git log --oneline origin/main`); this pipeline is the shape the next change takes.

A fix that changes what the receiver accepts, or a public name, is a breaking change: the spec of that is stage 01's last step, and the person decides before stage 02.

Stages, in order; inputs, outputs and checks for each are in [CONTEXT.md](CONTEXT.md):

1. [Reproduce](stages/01_reproduce/CONTEXT.md) — make it fail on purpose.
2. [Fix](stages/02_fix/CONTEXT.md) — change the cause, watch the reproduction pass.
3. [Verify](stages/03_verify/CONTEXT.md) — the checks, the pull request.
