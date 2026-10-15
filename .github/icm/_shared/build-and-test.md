---
verified_at: 2026-10-15
verified_commit: 337bb90fc61fd822113654f550d491de4e76aa38
---

# Build and test — the commands, and what CI runs

## Locally

- In a virtual environment: `pip install -e ".[dev]"` (pytest, pytest-asyncio, httpx, FastAPI, uvicorn: `pyproject.toml:18`), then `pytest tests/ -v`. Async tests run without markers (`asyncio_mode = "auto"`, `pyproject.toml:29`).
- `pip install build && python -m build` makes the sdist and wheel in `dist/`, as CI does.
- There is no linter or type checker configured; follow the style of the module you touch.

## Where a test belongs

One file per module: `tests/test_signature.py` (format and comparison), `tests/test_receiver.py` (each pipeline step and its status code, with deliveries signed by `sign_payload` and a current timestamp), `tests/test_fastapi.py` (the dependency through FastAPI's test client over httpx). No test reaches a network or a real secret.

## What CI runs

`ci.yml` on pull requests to `main` and pushes to `main`: the tests on Python 3.10, 3.11 and 3.12 (`.github/workflows/ci.yml:14`), then a build whose `dist/` is uploaded as an artifact. `publish.yml` runs the tests again before it publishes ([release.md](release.md)). `icm-check.yml` runs when an entry file or `.github/icm/` changes; CodeQL runs on its schedule.
