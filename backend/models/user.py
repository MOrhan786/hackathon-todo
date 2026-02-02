from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel

# Pydantic schemas for request/response validation
class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: str

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

class UserLogin(UserBase):
    """Schema for user login."""
    password: str

class UserResponse(UserBase):
    """Schema for returning user data (without password)."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Schema for updating user data."""
    email: Optional[str] = None
    password: Optional[str] = None

# SQLModel for database
class User(SQLModel, table=True):
    """User model for the database."""
    __table_args__ = {'extend_existing': True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255, index=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)