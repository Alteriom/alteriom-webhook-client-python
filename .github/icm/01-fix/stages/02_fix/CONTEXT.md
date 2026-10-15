# 02_fix — change the cause, not the symptom

One job: the smallest change at the defect's cause that turns the reproduction green without weakening any check.

## Inputs
- Working (this run): `.github/icm/01-fix/stages/01_reproduce/output/reproduction.md`
- Reference (every run): `.github/icm/_shared/architecture.md`
- Reference (every run): `.github/icm/_shared/build-and-test.md`

Do NOT load: the other pipeline, `.github/icm/_shared/release.md`, other runs' output.

## Process
1. Confirm the cause in the code before changing anything; if it moved, record where it really is.
2. Change the cause, within what the person approved at stage 01. The verification order stays as [architecture.md](../../../_shared/architecture.md) "The modules" lists it; no check is loosened, and the comparison stays constant-time.
3. A model change follows the TypeScript types in Alteriom/webhook-client or the delivery the person supplied: a new field is optional with a default; a new `Literal` value is added, not the `Literal` removed.
4. Keep `__all__` and every public signature unless the person approved otherwise. Do not edit the reproduction to make it pass.
5. Run the reproduction (green now), then `pytest tests/ -v` and `python -m build`.

## Outputs
- change.md → output/ — the cause in one paragraph; each file changed and why; the reproduction's passing output; the full test and build results; anything deliberately not addressed.

## Human check
A person reads the diff beside the reproduction: it removes the cause, no verification step was loosened or reordered, and any behaviour change is the one approved. Edit `change.md` if it is wrong; stage 03 reads it.
