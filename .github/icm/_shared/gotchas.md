---
verified_at: 2026-10-15
verified_commit: 337bb90fc61fd822113654f550d491de4e76aa38
---

# Gotchas — traps already in the code or the history

## Deliveries without an aggregate count as duplicates

The duplicate key is `subscription_id` plus the aggregate's id, or the literal `none` when there is no aggregate (`src/alteriom_webhook_client/receiver.py:131`). Within the cache's one-hour TTL, a second correctly signed delivery for the same subscription with no aggregate is therefore rejected with "Duplicate delivery detected" (401). Reproduced 2026-10-15: two deliveries with different `delivered_at` and no aggregate, the second refused. The TypeScript receiver in Alteriom/webhook-client builds its key the same way. Changing it changes what both SDKs accept: a decision, not a quiet fix.

## The signature is over the raw bytes

`verify_signature` signs the body exactly as received (`src/alteriom_webhook_client/signature.py:13`). Any framework code that parses and re-serialises the JSON before verifying will fail every signature; the FastAPI helper reads `request.body()` for that reason (`src/alteriom_webhook_client/fastapi.py`). Headers are matched case-insensitively (`receiver.py` lowercases them).

## Publishing is tied to names on PyPI's side

Trusted publishing (`.github/workflows/publish.yml:25`) works only while PyPI's trusted-publisher entry names this repository, `publish.yml` and the `pypi` environment. Renaming the workflow file or the environment breaks the next release at the upload, after the tests pass. Changing them is a release-day decision for a person, who also updates PyPI.

## The models refuse unknown enum values

`Enrichment.risk_level` and `WebhookEvent.processing_status` are `Literal`s (`src/alteriom_webhook_client/models.py`), so a new value the service starts sending fails validation with a 400 until the model follows. A delivery the receiver rejects for its shape, not its signature, is a `model-drift` report.
