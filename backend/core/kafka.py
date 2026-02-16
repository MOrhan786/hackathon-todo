"""
Kafka producer singleton with lazy initialization and graceful fallback.
"""
import asyncio
import logging
from typing import Optional

from aiokafka import AIOKafkaProducer
from core.config import settings

logger = logging.getLogger(__name__)

_producer: Optional[AIOKafkaProducer] = None
_lock = asyncio.Lock()


async def get_kafka_producer() -> Optional[AIOKafkaProducer]:
    """Get or create the Kafka producer singleton. Returns None if Kafka is disabled."""
    global _producer

    if not settings.KAFKA_ENABLED:
        return None

    if _producer is not None:
        return _producer

    async with _lock:
        if _producer is not None:
            return _producer

        try:
            _producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: v.encode("utf-8") if isinstance(v, str) else v,
                request_timeout_ms=5000,
                retry_backoff_ms=500,
            )
            await _producer.start()
            logger.info("Kafka producer connected to %s", settings.KAFKA_BOOTSTRAP_SERVERS)
        except Exception as e:
            logger.warning("Kafka producer failed to connect: %s. Events will be skipped.", e)
            _producer = None

    return _producer


async def close_kafka_producer():
    """Gracefully close the Kafka producer."""
    global _producer
    if _producer is not None:
        try:
            await _producer.stop()
            logger.info("Kafka producer closed.")
        except Exception as e:
            logger.warning("Error closing Kafka producer: %s", e)
        finally:
            _producer = None
