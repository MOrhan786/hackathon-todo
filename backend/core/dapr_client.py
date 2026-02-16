"""
HTTP client for Dapr sidecar operations (publish, state get/save).
"""
import json
import logging
from typing import Any, Dict, Optional

import httpx

from core.config import settings

logger = logging.getLogger(__name__)

DAPR_BASE_URL = f"http://localhost:{settings.DAPR_HTTP_PORT}/v1.0"


async def dapr_publish(topic: str, data: Dict[str, Any]):
    """Publish a message to a Dapr pub/sub topic."""
    url = f"{DAPR_BASE_URL}/publish/{settings.DAPR_PUBSUB_NAME}/{topic}"
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(url, json=data)
        response.raise_for_status()
        logger.debug("Dapr publish to %s/%s succeeded", settings.DAPR_PUBSUB_NAME, topic)


async def dapr_state_save(store_name: str, key: str, value: Any):
    """Save state via Dapr state store."""
    url = f"{DAPR_BASE_URL}/state/{store_name}"
    payload = [{"key": key, "value": value}]
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        logger.debug("Dapr state save to %s/%s succeeded", store_name, key)


async def dapr_state_get(store_name: str, key: str) -> Optional[Any]:
    """Get state from Dapr state store."""
    url = f"{DAPR_BASE_URL}/state/{store_name}/{key}"
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url)
        if response.status_code == 204:
            return None
        response.raise_for_status()
        return response.json()
