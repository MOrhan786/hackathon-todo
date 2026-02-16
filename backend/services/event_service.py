"""
Event publisher service for Kafka topics.

Publishes events to:
  - task-events: All CRUD operations
  - reminders: When reminder_at is set or modified
  - task-updates: Lightweight sync events for real-time updates

Supports dual mode:
  - Direct Kafka (KAFKA_ENABLED=true, DAPR_ENABLED=false)
  - Dapr HTTP sidecar (DAPR_ENABLED=true)
"""
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from core.config import settings

logger = logging.getLogger(__name__)

TOPIC_TASK_EVENTS = "task-events"
TOPIC_REMINDERS = "reminders"
TOPIC_TASK_UPDATES = "task-updates"


class UUIDEncoder(json.JSONEncoder):
    """JSON encoder that handles UUID and datetime objects."""
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def _serialize(data: Dict[str, Any]) -> str:
    return json.dumps(data, cls=UUIDEncoder)


async def publish_event(topic: str, event_type: str, data: Dict[str, Any]):
    """Publish an event to a Kafka topic using the active mode (direct or Dapr)."""
    if not settings.KAFKA_ENABLED and not settings.DAPR_ENABLED:
        return

    payload = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }

    try:
        if settings.DAPR_ENABLED:
            await _publish_via_dapr(topic, payload)
        else:
            await _publish_via_kafka(topic, payload)
    except Exception as e:
        logger.warning("Failed to publish event %s to %s: %s", event_type, topic, e)


async def _publish_via_kafka(topic: str, payload: Dict[str, Any]):
    """Publish directly to Kafka using aiokafka producer."""
    from core.kafka import get_kafka_producer

    producer = await get_kafka_producer()
    if producer is None:
        logger.debug("Kafka producer unavailable, skipping event.")
        return

    message = _serialize(payload)
    await producer.send_and_wait(topic, message.encode("utf-8"))
    logger.debug("Published to Kafka topic %s: %s", topic, payload["event_type"])


async def _publish_via_dapr(topic: str, payload: Dict[str, Any]):
    """Publish via Dapr sidecar HTTP API."""
    from core.dapr_client import dapr_publish

    await dapr_publish(topic, payload)
    logger.debug("Published via Dapr to topic %s: %s", topic, payload["event_type"])


async def emit_task_created(task_data: Dict[str, Any], user_id: str):
    """Emit event when a task is created."""
    event_data = {"task": task_data, "user_id": user_id}
    await publish_event(TOPIC_TASK_EVENTS, "task.created", event_data)
    await publish_event(TOPIC_TASK_UPDATES, "task.created", {"task_id": task_data.get("id"), "user_id": user_id})

    if task_data.get("reminder_at"):
        await publish_event(TOPIC_REMINDERS, "reminder.scheduled", event_data)


async def emit_task_updated(task_data: Dict[str, Any], user_id: str):
    """Emit event when a task is updated."""
    event_data = {"task": task_data, "user_id": user_id}
    await publish_event(TOPIC_TASK_EVENTS, "task.updated", event_data)
    await publish_event(TOPIC_TASK_UPDATES, "task.updated", {"task_id": task_data.get("id"), "user_id": user_id})

    if task_data.get("reminder_at"):
        await publish_event(TOPIC_REMINDERS, "reminder.scheduled", event_data)


async def emit_task_deleted(task_id: str, user_id: str):
    """Emit event when a task is deleted."""
    event_data = {"task_id": task_id, "user_id": user_id}
    await publish_event(TOPIC_TASK_EVENTS, "task.deleted", event_data)
    await publish_event(TOPIC_TASK_UPDATES, "task.deleted", event_data)


async def emit_task_toggled(task_data: Dict[str, Any], user_id: str):
    """Emit event when a task is toggled."""
    event_data = {"task": task_data, "user_id": user_id}
    await publish_event(TOPIC_TASK_EVENTS, "task.toggled", event_data)
    await publish_event(TOPIC_TASK_UPDATES, "task.toggled", {"task_id": task_data.get("id"), "status": task_data.get("status"), "user_id": user_id})
