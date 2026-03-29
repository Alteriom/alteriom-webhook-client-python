"""FastAPI integration for webhook verification.

Usage::

    from alteriom_webhook_client.fastapi import webhook_receiver
    from alteriom_webhook_client.models import SubscriptionDelivery

    verify = webhook_receiver(secret=os.getenv("WEBHOOK_SECRET"))

    @app.post("/webhook")
    async def handle(delivery: SubscriptionDelivery = Depends(verify)):
        print(delivery.aggregate.repository)
"""

from typing import Callable

from fastapi import HTTPException, Request

from .models import SubscriptionDelivery
from .receiver import WebhookReceiver, WebhookVerificationError


def webhook_receiver(
    secret: str,
    max_age_ms: int = 300_000,
    max_payload_bytes: int = 10_485_760,
) -> Callable:
    """Create a FastAPI dependency for webhook verification."""
    receiver = WebhookReceiver(
        secret=secret,
        max_age_ms=max_age_ms,
        max_payload_bytes=max_payload_bytes,
    )

    async def dependency(request: Request) -> SubscriptionDelivery:
        body = await request.body()
        headers = dict(request.headers)

        try:
            return receiver.receive(body, headers)
        except WebhookVerificationError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)

    return dependency
