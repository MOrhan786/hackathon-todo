from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel

# Pydantic schemas for request/response validation
class TodoBase(BaseModel):
    """Base todo schema with common fields."""
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    """Schema for creating a new todo."""
    pass

class TodoUpdate(BaseModel):
    """Schema for updating a todo."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    """Schema for returning todo data."""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# SQLModel for database
class Todo(SQLModel, table=True):
    """Todo model for the database."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)