"""Webhook receiver — placeholder for future implementation."""


class WebhookVerificationError(Exception):
    """Raised when webhook signature verification fails."""


class WebhookReceiver:
    """Receives and verifies incoming webhook deliveries."""

    def __init__(self, secret: str) -> None:
        self.secret = secret
