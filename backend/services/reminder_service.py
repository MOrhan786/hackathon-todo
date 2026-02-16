from sqlmodel import Session, select
from typing import List
from uuid import UUID
from models.reminder import TaskReminder
from models.task import Task
from schemas.reminder import ReminderCreate
from utils.errors import TaskNotFoundError, UnauthorizedAccessError
from datetime import datetime


class ReminderService:
    """Service class for handling task reminder operations."""

    @staticmethod
    def create_reminder(session: Session, task_id: UUID, reminder_data: ReminderCreate, user_id: str) -> TaskReminder:
        """Create a new reminder for a task owned by the user."""
        # Verify task exists and belongs to user
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(str(task_id))

        stored_user_id = str(task.user_id).lower() if task.user_id else ""
        requested_user_id = str(user_id).lower() if user_id else ""

        if stored_user_id != requested_user_id:
            raise UnauthorizedAccessError(str(task_id), user_id)

        reminder = TaskReminder(
            task_id=task_id,
            user_id=user_id,
            remind_at=reminder_data.remind_at,
            is_sent=False
        )

        session.add(reminder)
        session.commit()
        session.refresh(reminder)
        return reminder

    @staticmethod
    def get_reminders_by_user(session: Session, user_id: str) -> List[TaskReminder]:
        """Get all reminders for a user."""
        statement = select(TaskReminder).where(
            TaskReminder.user_id == user_id
        ).order_by(TaskReminder.remind_at)
        return session.exec(statement).all()

    @staticmethod
    def get_reminders_by_task(session: Session, task_id: UUID, user_id: str) -> List[TaskReminder]:
        """Get all reminders for a specific task owned by the user."""
        statement = select(TaskReminder).where(
            TaskReminder.task_id == task_id,
            TaskReminder.user_id == user_id
        ).order_by(TaskReminder.remind_at)
        return session.exec(statement).all()

    @staticmethod
    def delete_reminder(session: Session, reminder_id: UUID, user_id: str) -> bool:
        """Delete a reminder if it belongs to the user."""
        statement = select(TaskReminder).where(TaskReminder.id == reminder_id)
        reminder = session.exec(statement).first()

        if not reminder:
            raise TaskNotFoundError(str(reminder_id))

        if str(reminder.user_id).lower() != str(user_id).lower():
            raise UnauthorizedAccessError(str(reminder_id), user_id)

        session.delete(reminder)
        session.commit()
        return True
