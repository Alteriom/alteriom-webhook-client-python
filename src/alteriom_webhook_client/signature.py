"""Low-level HMAC-SHA256 signature functions.

Matches the TypeScript @alteriom/webhook-client SDK signature format:
  HMAC-SHA256("{timestamp}.{body}") -> "sha256={hex}"
"""

import hashlib
import hmac as _hmac


def sign_payload(body: bytes, timestamp: str, secret: str) -> str:
    """Generate HMAC-SHA256 signature for a webhook payload."""
    data = f"{timestamp}.".encode() + body
    digest = _hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def verify_signature(body: bytes, signature: str, timestamp: str, secret: str) -> bool:
    """Verify HMAC-SHA256 signature using timing-safe comparison."""
    expected = sign_payload(body, timestamp, secret)
    return _hmac.compare_digest(signature, expected)
