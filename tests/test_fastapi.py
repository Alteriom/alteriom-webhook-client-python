"""Tests for FastAPI integration."""

import json
import time

import pytest
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient

from alteriom_webhook_client.fastapi import webhook_receiver
from alteriom_webhook_client.models import SubscriptionDelivery
from alteriom_webhook_client.signature import sign_payload

SECRET = "fastapi-test-secret"

PAYLOAD = {
    "subscription_id": "sub-1",
    "aggregate": {
        "id": "agg-1",
        "repository": "owner/repo",
        "entity_type": "pull_request",
        "entity_id": "owner/repo#1",
        "aggregate_type": "pull_request",
        "summary": {},
    },
    "delivered_at": "2026-03-29T00:00:00Z",
}


def build_app() -> FastAPI:
    app = FastAPI()
    verify = webhook_receiver(secret=SECRET)

    @app.post("/webhook")
    async def handle(delivery: SubscriptionDelivery = Depends(verify)):
        return {"subscription_id": delivery.subscription_id, "ok": True}

    return app


def signed_headers(body: bytes) -> dict[str, str]:
    ts = str(int(time.time() * 1000))
    sig = sign_payload(body, ts, SECRET)
    return {
        "x-connector-signature-256": sig,
        "x-connector-timestamp": ts,
        "content-type": "application/json",
    }


@pytest.mark.asyncio
async def test_valid_delivery():
    app = build_app()
    body = json.dumps(PAYLOAD).encode()
    headers = signed_headers(body)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/webhook", content=body, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["subscription_id"] == "sub-1"
    assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_missing_signature_returns_401():
    app = build_app()
    body = json.dumps(PAYLOAD).encode()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/webhook", content=body, headers={"content-type": "application/json"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_bad_signature_returns_401():
    app = build_app()
    body = json.dumps(PAYLOAD).encode()
    ts = str(int(time.time() * 1000))
    headers = {
        "x-connector-signature-256": "sha256=0000000000000000000000000000000000000000000000000000000000000000",
        "x-connector-timestamp": ts,
        "content-type": "application/json",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/webhook", content=body, headers=headers)
    assert resp.status_code == 401
