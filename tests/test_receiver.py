"""Tests for WebhookReceiver."""

import json
import time

from alteriom_webhook_client.receiver import WebhookReceiver, WebhookVerificationError
from alteriom_webhook_client.signature import sign_payload

SECRET = "test-secret-key"
DELIVERY_PAYLOAD = {
    "subscription_id": "sub-123",
    "aggregate": {
        "id": "agg-1",
        "repository": "owner/repo",
        "entity_type": "pull_request",
        "entity_id": "owner/repo#42",
        "aggregate_type": "pull_request",
        "summary": {"title": "Fix bug", "number": 42},
    },
    "delivered_at": "2026-03-29T12:00:00Z",
}


def make_signed_request(
    payload: dict = DELIVERY_PAYLOAD,
    secret: str = SECRET,
    timestamp_ms: int | None = None,
) -> tuple[bytes, dict[str, str]]:
    body = json.dumps(payload).encode()
    ts = str(timestamp_ms or int(time.time() * 1000))
    sig = sign_payload(body, ts, secret)
    headers = {
        "x-connector-signature-256": sig,
        "x-connector-timestamp": ts,
        "content-type": "application/json",
    }
    return body, headers


class TestReceiveValid:
    def test_returns_subscription_delivery(self):
        receiver = WebhookReceiver(secret=SECRET)
        body, headers = make_signed_request()
        delivery = receiver.receive(body, headers)
        assert delivery.subscription_id == "sub-123"
        assert delivery.aggregate is not None
        assert delivery.aggregate.repository == "owner/repo"
        assert delivery.aggregate.entity_type == "pull_request"

    def test_delivery_with_no_aggregate(self):
        receiver = WebhookReceiver(secret=SECRET)
        payload = {"subscription_id": "sub-1", "delivered_at": "2026-03-29T00:00:00Z"}
        body, headers = make_signed_request(payload=payload)
        delivery = receiver.receive(body, headers)
        assert delivery.aggregate is None


class TestReceiveMissingHeaders:
    def test_missing_signature_raises_401(self):
        receiver = WebhookReceiver(secret=SECRET)
        body = b'{"subscription_id":"sub-1","delivered_at":"now"}'
        headers = {"x-connector-timestamp": "1711700000000"}
        try:
            receiver.receive(body, headers)
            assert False, "Should have raised"
        except WebhookVerificationError as e:
            assert e.status_code == 401
            assert "signature" in e.message.lower()

    def test_missing_timestamp_raises_401(self):
        receiver = WebhookReceiver(secret=SECRET)
        body = b'{"subscription_id":"sub-1","delivered_at":"now"}'
        headers = {"x-connector-signature-256": "sha256=abc"}
        try:
            receiver.receive(body, headers)
            assert False, "Should have raised"
        except WebhookVerificationError as e:
            assert e.status_code == 401
            assert "timestamp" in e.message.lower()


class TestReceiveBadSignature:
    def test_wrong_secret_raises_401(self):
        receiver = WebhookReceiver(secret=SECRET)
        body, headers = make_signed_request(secret="wrong-secret")
        try:
            receiver.receive(body, headers)
            assert False, "Should have raised"
        except WebhookVerificationError as e:
            assert e.status_code == 401
            assert "signature" in e.message.lower()


class TestReceiveTimestamp:
    def test_expired_timestamp_raises_401(self):
        receiver = WebhookReceiver(secret=SECRET, max_age_ms=1000)
        old_ts = int(time.time() * 1000) - 5000
        body, headers = make_signed_request(timestamp_ms=old_ts)
        try:
            receiver.receive(body, headers)
            assert False, "Should have raised"
        except WebhookVerificationError as e:
            assert e.status_code == 401


class TestReceivePayloadSize:
    def test_oversized_payload_raises_413(self):
        receiver = WebhookReceiver(secret=SECRET, max_payload_bytes=100)
        large_payload = {"subscription_id": "sub-1", "delivered_at": "now", "data": "x" * 200}
        body, headers = make_signed_request(payload=large_payload)
        try:
            receiver.receive(body, headers)
            assert False, "Should have raised"
        except WebhookVerificationError as e:
            assert e.status_code == 413


class TestReceiveDuplicate:
    def test_duplicate_delivery_raises_401(self):
        receiver = WebhookReceiver(secret=SECRET)
        body, headers = make_signed_request()
        receiver.receive(body, headers)
        body2, headers2 = make_signed_request()
        try:
            receiver.receive(body2, headers2)
            assert False, "Should have raised"
        except WebhookVerificationError as e:
            assert e.status_code == 401
            assert "duplicate" in e.message.lower()
