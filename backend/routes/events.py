"""
Dapr subscription and event handler endpoints.

These endpoints are called by Dapr when events are published to subscribed topics.
Also includes a cron handler for periodic reminder checks.
"""
import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/task-events")
async def handle_task_event(request: Request):
    """Handle task CRUD events from Dapr pub/sub."""
    try:
        body = await request.json()
        event_data = body.get("data", body)
        event_type = event_data.get("event_type", "unknown")
        logger.info("Received task event: %s", event_type)
        return JSONResponse(content={"status": "SUCCESS"})
    except Exception as e:
        logger.error("Error handling task event: %s", e)
        return JSONResponse(content={"status": "RETRY"}, status_code=500)


@router.post("/reminders")
async def handle_reminder_event(request: Request):
    """Handle reminder events from Dapr pub/sub."""
    try:
        body = await request.json()
        event_data = body.get("data", body)
        event_type = event_data.get("event_type", "unknown")
        logger.info("Received reminder event: %s", event_type)
        return JSONResponse(content={"status": "SUCCESS"})
    except Exception as e:
        logger.error("Error handling reminder event: %s", e)
        return JSONResponse(content={"status": "RETRY"}, status_code=500)


@router.post("/task-updates")
async def handle_task_update(request: Request):
    """Handle lightweight task update events from Dapr pub/sub."""
    try:
        body = await request.json()
        event_data = body.get("data", body)
        event_type = event_data.get("event_type", "unknown")
        logger.info("Received task update event: %s", event_type)
        return JSONResponse(content={"status": "SUCCESS"})
    except Exception as e:
        logger.error("Error handling task update event: %s", e)
        return JSONResponse(content={"status": "RETRY"}, status_code=500)


@router.post("/cron/check-reminders")
async def cron_check_reminders():
    """
    Dapr cron binding handler. Called periodically (every 5 minutes) to check for due reminders.
    """
    logger.info("Cron: checking for due reminders")
    try:
        from sqlmodel import Session, select
        from models.task import Task
        from datetime import datetime
        from core.db import engine
        from services.event_service import publish_event, TOPIC_REMINDERS

        now = datetime.utcnow()

        with Session(engine) as session:
            statement = select(Task).where(
                Task.is_deleted == False,
                Task.reminder_at <= now,
                Task.reminder_sent == False,
                Task.status != "completed",
            )
            due_tasks = session.exec(statement).all()

            for task in due_tasks:
                try:
                    await publish_event(
                        TOPIC_REMINDERS,
                        "reminder.due",
                        {"task_id": str(task.id), "user_id": task.user_id, "title": task.title},
                    )
                except Exception as pub_err:
                    logger.warning("Failed to publish reminder for task %s: %s", task.id, pub_err)

                task.reminder_sent = True
                session.add(task)

            session.commit()
            logger.info("Cron: processed %d due reminders", len(due_tasks))

        return JSONResponse(content={"status": "SUCCESS"})
    except Exception as e:
        logger.error("Cron reminder check failed: %s", e)
        return JSONResponse(content={"status": "RETRY"}, status_code=500)
