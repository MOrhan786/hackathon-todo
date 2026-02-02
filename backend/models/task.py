from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func
from typing import Optional
import uuid
from datetime import datetime


class TaskBase(SQLModel):
    """
    Base class for Task model containing common fields.
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default="", max_length=1000)
    status: str = Field(default="pending", regex="^(pending|completed)$")


class Task(TaskBase, table=True):
    """
    Task model representing a user's todo item.

    Attributes:
        id: Unique identifier for the task
        title: Task title (1-255 characters)
        description: Optional task description (max 1000 characters)
        status: Task status ('pending' or 'completed')
        user_id: ID of the user who owns the task
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
    """
    __tablename__ = "tasks"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False
    )
    user_id: str = Field(index=True)  # Foreign key reference to user
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )


class TaskCreate(TaskBase):
    """
    Model for creating a new task.

    Requires title, with optional description and status (defaults to 'pending').
    """
    pass


class TaskUpdate(SQLModel):
    """
    Model for updating an existing task.

    All fields are optional for partial updates.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[str] = Field(default=None, regex="^(pending|completed)$")


class TaskRead(TaskBase):
    """
    Model for reading task data with ID and timestamps.
    """
    id: uuid.UUID
    user_id: str
    created_at: datetime
    updated_at: datetime