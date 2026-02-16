from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func, JSON, String
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
import enum


class TaskStatus(str, enum.Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, enum.Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class RecurrencePattern(str, enum.Enum):
    """Recurrence pattern for recurring tasks."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class TaskBase(SQLModel):
    """
    Base class for Task model containing common fields.
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default="", max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)
    tags: List[str] = Field(default=[], sa_column=Column(JSON, default=[]))
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None, max_length=20)
    recurrence_interval: int = Field(default=1)
    recurrence_end_date: Optional[datetime] = Field(default=None)
    reminder_at: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """
    Task model representing a user's todo item.

    Attributes:
        id: Unique identifier for the task
        title: Task title (1-255 characters)
        description: Optional task description (max 1000 characters)
        status: Task status (pending/in_progress/completed)
        priority: Task priority (low/medium/high/urgent)
        due_date: Optional due date for the task
        tags: List of tag strings for categorization
        is_recurring: Whether task repeats on a schedule
        recurrence_pattern: daily/weekly/monthly/yearly
        recurrence_interval: Number of pattern units between occurrences
        recurrence_end_date: When recurrence stops
        reminder_at: When to send a reminder notification
        user_id: ID of the user who owns the task
        completed_at: Timestamp when the task was completed
        is_deleted: Soft delete flag
        reminder_sent: Whether reminder notification was sent
        parent_task_id: ID of the parent recurring task (for generated occurrences)
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
    """
    __tablename__ = "tasks"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )
    user_id: str = Field(index=True)
    completed_at: Optional[datetime] = Field(default=None)
    is_deleted: bool = Field(default=False, index=True)
    reminder_sent: bool = Field(default=False)
    parent_task_id: Optional[UUID] = Field(default=None, index=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )


class TaskCreate(TaskBase):
    """
    Model for creating a new task.

    Requires title, with optional description, status, priority, due_date,
    tags, recurrence settings, and reminder.
    """
    pass


class TaskUpdate(SQLModel):
    """
    Model for updating an existing task.

    All fields are optional for partial updates.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    recurrence_end_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None


class TaskRead(TaskBase):
    """
    Model for reading task data with ID and timestamps.
    """
    id: UUID
    user_id: str
    completed_at: Optional[datetime]
    is_deleted: bool
    reminder_sent: bool
    parent_task_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
