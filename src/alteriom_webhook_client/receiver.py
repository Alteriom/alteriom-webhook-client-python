"""WebhookReceiver — full verification pipeline for incoming webhook deliveries.

Validates: payload size, headers, timestamp freshness, HMAC signature,
duplicate detection. Parses into SubscriptionDelivery model.
"""

from __future__ import annotations

import json
import time
from collections import OrderedDict

from .models import SubscriptionDelivery
from .signature import verify_signature


class WebhookVerificationError(Exception):
    """Raised when webhook verification fails."""

    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class _LRUCache:
    """Simple LRU cache with TTL for duplicate detection."""

    def __init__(self, max_size: int = 10_000, ttl_ms: int = 3_600_000):
        self._max_size = max_size
        self._ttl_ms = ttl_ms
        self._cache: OrderedDict[str, float] = OrderedDict()

    def contains(self, key: str) -> bool:
        if key in self._cache:
            ts = self._cache[key]
            if (time.time() * 1000 - ts) < self._ttl_ms:
                self._cache.move_to_end(key)
                return True
            else:
                del self._cache[key]
        return False

    def add(self, key: str) -> None:
        self._cache[key] = time.time() * 1000
        self._cache.move_to_end(key)
        while len(self._cache) > self._max_size:
            self._cache.popitem(last=False)


class WebhookReceiver:
    """Verify and parse incoming webhook deliveries.

    Args:
        secret: HMAC shared secret for signature verification.
        max_age_ms: Maximum allowed age of timestamp (default 5 minutes).
        max_payload_bytes: Maximum payload size (default 10 MB).
    """

    def __init__(
        self,
        secret: str,
        max_age_ms: int = 300_000,
        max_payload_bytes: int = 10_485_760,
    ):
        self._secret = secret
        self._max_age_ms = max_age_ms
        self._max_payload_bytes = max_payload_bytes
        self._seen = _LRUCache()

    def receive(self, body: bytes, headers: dict[str, str]) -> SubscriptionDelivery:
        """Verify and parse a webhook delivery.

        Args:
            body: Raw request body bytes.
            headers: HTTP headers dict (keys should be lowercase).

        Returns:
            Parsed SubscriptionDelivery.

        Raises:
            WebhookVerificationError: On verification failure.
        """
        h = {k.lower(): v for k, v in headers.items()}

        # 1. Payload size check
        if len(body) > self._max_payload_bytes:
            raise WebhookVerificationError(
                f"Payload too large: {len(body)} bytes (max {self._max_payload_bytes})",
                status_code=413,
            )

        # 2. Extract required headers
        signature = h.get("x-connector-signature-256")
        timestamp = h.get("x-connector-timestamp")

        if not signature:
            raise WebhookVerificationError("Missing x-connector-signature-256 header")
        if not timestamp:
            raise WebhookVerificationError("Missing x-connector-timestamp header")

        # 3. Timestamp freshness
        try:
            ts_ms = int(timestamp)
        except ValueError:
            raise WebhookVerificationError("Invalid timestamp format")

        age_ms = int(time.time() * 1000) - ts_ms
        if age_ms > self._max_age_ms:
            raise WebhookVerificationError(
                f"Timestamp expired: {age_ms}ms old (max {self._max_age_ms}ms)"
            )

        # 4. Signature verification
        if not verify_signature(body, signature, timestamp, self._secret):
            raise WebhookVerificationError("Invalid signature")

        # 5. Parse payload
        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            raise WebhookVerificationError(f"Invalid JSON: {e}", status_code=400)

        try:
            delivery = SubscriptionDelivery.model_validate(data)
        except Exception as e:
            raise WebhookVerificationError(f"Invalid payload: {e}", status_code=400)

        # 6. Duplicate detection
        agg_id = delivery.aggregate.id if delivery.aggregate else "none"
        dedup_key = f"{delivery.subscription_id}:{agg_id}"
        if self._seen.contains(dedup_key):
            raise WebhookVerificationError("Duplicate delivery detected")
        self._seen.add(dedup_key)

        return delivery
