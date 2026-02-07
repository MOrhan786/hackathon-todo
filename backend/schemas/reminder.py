from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class ReminderCreate(BaseModel):
    """
    Schema for creating a new reminder.

    Requires remind_at timestamp.
    """
    remind_at: datetime


class ReminderResponse(BaseModel):
    """
    Schema for reminder response with all fields.
    """
    id: UUID
    task_id: UUID
    user_id: str
    remind_at: datetime
    is_sent: bool
    sent_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ReminderListResponse(BaseModel):
    """
    Schema for listing reminders response.
    """
    reminders: List[ReminderResponse]
    total: int = 0
