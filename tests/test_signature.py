"""Tests for signature verification and signing."""

import hmac
import hashlib

from alteriom_webhook_client.signature import sign_payload, verify_signature


class TestSignPayload:
    def test_generates_sha256_prefixed_signature(self):
        body = b'{"event":"push"}'
        timestamp = "1711700000000"
        secret = "test-secret"
        sig = sign_payload(body, timestamp, secret)
        assert sig.startswith("sha256=")
        assert len(sig) == 7 + 64

    def test_uses_timestamp_dot_body_format(self):
        body = b'{"event":"push"}'
        timestamp = "1711700000000"
        secret = "test-secret"
        data = f"{timestamp}.".encode() + body
        expected_hex = hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()
        sig = sign_payload(body, timestamp, secret)
        assert sig == f"sha256={expected_hex}"


class TestVerifySignature:
    def test_valid_signature_returns_true(self):
        body = b'{"subscription_id":"sub-1","delivered_at":"2026-03-29"}'
        timestamp = "1711700000000"
        secret = "my-webhook-secret"
        sig = sign_payload(body, timestamp, secret)
        assert verify_signature(body, sig, timestamp, secret) is True

    def test_wrong_secret_returns_false(self):
        body = b'{"event":"push"}'
        timestamp = "1711700000000"
        sig = sign_payload(body, timestamp, "correct-secret")
        assert verify_signature(body, sig, timestamp, "wrong-secret") is False

    def test_tampered_body_returns_false(self):
        body = b'{"event":"push"}'
        timestamp = "1711700000000"
        secret = "test-secret"
        sig = sign_payload(body, timestamp, secret)
        assert verify_signature(b'{"event":"tampered"}', sig, timestamp, secret) is False

    def test_malformed_signature_returns_false(self):
        body = b'{"event":"push"}'
        timestamp = "1711700000000"
        assert verify_signature(body, "not-a-valid-sig", timestamp, "test-secret") is False

    def test_empty_body(self):
        body = b""
        timestamp = "1711700000000"
        secret = "test-secret"
        sig = sign_payload(body, timestamp, secret)
        assert verify_signature(body, sig, timestamp, secret) is True
