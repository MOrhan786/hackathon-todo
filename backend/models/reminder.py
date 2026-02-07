from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class TaskReminderBase(SQLModel):
    """Base class for TaskReminder model."""
    remind_at: datetime


class TaskReminder(TaskReminderBase, table=True):
    """
    TaskReminder model representing a scheduled reminder for a task.

    Attributes:
        id: Unique identifier for the reminder
        task_id: ID of the associated task
        user_id: ID of the user who owns the reminder (denormalized)
        remind_at: When to send the reminder
        is_sent: Whether the reminder has been sent
        sent_at: When the reminder was sent
        created_at: Timestamp when the reminder was created
    """
    __tablename__ = "task_reminders"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )
    task_id: UUID = Field(foreign_key="tasks.id", index=True)
    user_id: str = Field(index=True)
    is_sent: bool = Field(default=False)
    sent_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )


class ReminderCreate(TaskReminderBase):
    """Model for creating a new reminder."""
    pass


class ReminderRead(TaskReminderBase):
    """Model for reading reminder data."""
    id: UUID
    task_id: UUID
    user_id: str
    is_sent: bool
    sent_at: Optional[datetime]
    created_at: datetime
