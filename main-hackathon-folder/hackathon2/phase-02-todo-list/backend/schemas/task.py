from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid


class TaskBase(BaseModel):
    """
    Base schema for task operations.
    """
    title: str
    description: Optional[str] = ""
    status: str = "pending"


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.

    Requires title, with optional description and status (defaults to 'pending').
    """
    title: str
    description: Optional[str] = ""
    status: str = "pending"


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    All fields are optional for partial updates.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(TaskBase):
    """
    Schema for task response with additional fields.
    """
    id: uuid.UUID
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """
    Schema for listing tasks response.
    """
    tasks: List[TaskResponse]