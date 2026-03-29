"""Pydantic v2 models for webhook delivery payloads.

Mirrors the TypeScript @alteriom/webhook-client SubscriptionDelivery type.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class Enrichment(BaseModel):
    """AI enrichment data attached to an aggregate."""
    summary: str
    risk_level: Literal["low", "medium", "high", "critical"]
    complexity: float
    security_concerns: list[str] = []
    suggested_actions: list[str] = []
    cost_usd: float | None = None


class Aggregate(BaseModel):
    """Event aggregate — a grouped view of related webhook events."""
    id: str
    repository: str
    entity_type: str
    entity_id: str
    aggregate_type: str
    summary: dict[str, Any] = {}
    enrichment: Enrichment | None = None
    event_count: int | None = None
    first_event_at: str | None = None
    last_event_at: str | None = None


class WebhookEvent(BaseModel):
    """A single webhook event within a delivery."""
    id: str
    event_type: str
    action: str | None = None
    repository: str | None = None
    sender: str | None = None
    github_delivery_id: str
    payload: dict[str, Any] = {}
    received_at: str
    processing_status: Literal["pending", "completed", "failed"]
    processing_error: str | None = None


class SubscriptionDelivery(BaseModel):
    """A webhook delivery payload sent by the connector to subscribers."""
    subscription_id: str
    aggregate: Aggregate | None = None
    events: list[WebhookEvent] | None = None
    delivered_at: str
