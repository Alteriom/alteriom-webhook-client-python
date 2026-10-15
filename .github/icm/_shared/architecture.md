---
verified_at: 2026-10-15
verified_commit: 337bb90fc61fd822113654f550d491de4e76aa38
---

# Architecture — where each part of the package lives

## The modules

- `src/alteriom_webhook_client/signature.py` — `sign_payload` and `verify_signature`: HMAC-SHA256 over `"{timestamp}." + body` (the raw bytes), as `sha256=<hex>`, compared with `hmac.compare_digest`.
- `src/alteriom_webhook_client/receiver.py` — `WebhookReceiver.receive` (`src/alteriom_webhook_client/receiver.py:71`) runs the pipeline in order: payload size (413), the two signature headers, timestamp age, signature, JSON, model validation (400 for both), then duplicate detection (`src/alteriom_webhook_client/receiver.py:129`) in an in-memory LRU with a one-hour TTL (`src/alteriom_webhook_client/receiver.py:26`). Every failure is a `WebhookVerificationError` with a status code.
- `src/alteriom_webhook_client/models.py` — Pydantic v2 models `SubscriptionDelivery`, `Aggregate`, `Enrichment`, `WebhookEvent`.
- `src/alteriom_webhook_client/fastapi.py` — `webhook_receiver(...)` returns a FastAPI dependency that reads the raw body and turns the error into an `HTTPException`. FastAPI is an optional extra (`pyproject.toml:17`); only this module imports it.
- `src/alteriom_webhook_client/__init__.py` — the public names (`__all__`); the FastAPI helper is imported from its own module.

## What it must agree with

The signature format and the delivery models mirror the TypeScript package in Alteriom/webhook-client (its `src/receiver.ts` and `src/types.ts`), as the module docstrings say (`src/alteriom_webhook_client/signature.py:3`, `src/alteriom_webhook_client/models.py:3`). The service that sends the deliveries is private: a model or header change starts from the TypeScript package or from a delivery the person supplies, never from guesses about the service.

## The package

Hatchling builds the wheel from `src/alteriom_webhook_client` (`pyproject.toml:26`). The only runtime dependency is `pydantic>=2.0` (`pyproject.toml:12`); Python 3.10 or later (`pyproject.toml:11`). The version is `pyproject.toml:7`; the package does not expose `__version__`.
