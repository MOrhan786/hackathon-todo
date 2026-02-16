"""
Standalone Kafka consumer for processing reminder notifications.

Runs as a separate process/container, consuming from the 'reminders' topic.
This consumer is fully self-contained — it does NOT import core.config or any
backend modules that require DATABASE_URL/JWT secrets.
"""
import asyncio
import json
import logging
import os
import signal

from aiokafka import AIOKafkaConsumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("notification-consumer")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = "reminders"
GROUP_ID = "notification-consumer-group"

shutdown_event = asyncio.Event()


async def process_reminder(message: dict):
    """Process a reminder event. Extend this to send emails, push notifications, etc."""
    event_type = message.get("event_type", "unknown")
    data = message.get("data", {})
    task_id = data.get("task_id", "unknown")
    user_id = data.get("user_id", "unknown")
    title = data.get("title", "Untitled")

    logger.info(
        "Processing reminder [%s] task=%s user=%s title='%s'",
        event_type, task_id, user_id, title,
    )

    # Future: integrate with email, SMS, push notification services
    logger.info("NOTIFICATION: Reminder due for task '%s' (user: %s)", title, user_id)


async def consume():
    """Main consumer loop with graceful shutdown."""
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    logger.info("Starting notification consumer, connecting to %s", KAFKA_BOOTSTRAP_SERVERS)

    # Retry connection with backoff
    for attempt in range(1, 11):
        try:
            await consumer.start()
            logger.info("Notification consumer started, listening on topic '%s'", TOPIC)
            break
        except Exception as e:
            wait = min(attempt * 5, 30)
            logger.warning("Connection attempt %d failed: %s. Retrying in %ds...", attempt, e, wait)
            await asyncio.sleep(wait)
    else:
        logger.error("Failed to connect to Kafka after 10 attempts. Exiting.")
        return

    try:
        async for msg in consumer:
            if shutdown_event.is_set():
                break
            try:
                await process_reminder(msg.value)
            except Exception as e:
                logger.error("Error processing message: %s", e)
    finally:
        await consumer.stop()
        logger.info("Notification consumer stopped.")


def main():
    loop = asyncio.new_event_loop()

    def handle_signal():
        logger.info("Received shutdown signal")
        shutdown_event.set()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, handle_signal)

    try:
        loop.run_until_complete(consume())
    finally:
        loop.close()


if __name__ == "__main__":
    main()
