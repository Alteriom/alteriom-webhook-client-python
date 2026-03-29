# alteriom-webhook-client

Python SDK for the [Alteriom Webhook Connector](https://github.com/Alteriom/alteriom-webhook-connector). Provides HMAC-SHA256 signature verification, Pydantic models for delivery payloads, and a FastAPI integration helper.

## Installation

```bash
pip install alteriom-webhook-client

# With FastAPI integration
pip install alteriom-webhook-client[fastapi]
```

## Quick Start (FastAPI)

```python
import os
from fastapi import Depends, FastAPI
from alteriom_webhook_client.fastapi import webhook_receiver
from alteriom_webhook_client.models import SubscriptionDelivery

app = FastAPI()
verify = webhook_receiver(secret=os.getenv("WEBHOOK_SECRET"))

@app.post("/webhook")
async def handle_webhook(delivery: SubscriptionDelivery = Depends(verify)):
    if delivery.aggregate:
        print(f"Got {delivery.aggregate.entity_type} for {delivery.aggregate.repository}")
    return {"status": "accepted"}
```

## Manual Usage

```python
from alteriom_webhook_client import WebhookReceiver, WebhookVerificationError

receiver = WebhookReceiver(secret="your-secret")

# In any framework:
try:
    delivery = receiver.receive(body=request_body_bytes, headers=request_headers_dict)
    print(delivery.subscription_id)
    print(delivery.aggregate.summary)
except WebhookVerificationError as e:
    print(f"Verification failed: {e.message} (HTTP {e.status_code})")
```

## Low-Level Signature Functions

```python
from alteriom_webhook_client import verify_signature, sign_payload

# Verify a signature
is_valid = verify_signature(
    body=raw_bytes,
    signature=headers["x-connector-signature-256"],
    timestamp=headers["x-connector-timestamp"],
    secret="your-secret",
)

# Generate a signature (for testing)
sig = sign_payload(body=raw_bytes, timestamp="1711700000000", secret="your-secret")
```

## Configuration

```python
receiver = WebhookReceiver(
    secret="your-secret",
    max_age_ms=300_000,          # Reject timestamps older than 5 minutes (default)
    max_payload_bytes=10_485_760, # Reject payloads larger than 10 MB (default)
)
```

## Models

- `SubscriptionDelivery` — top-level delivery payload
- `Aggregate` — event aggregate (PR lifecycle, issue, workflow, etc.)
- `Enrichment` — AI enrichment data
- `WebhookEvent` — individual webhook event

## License

MIT
