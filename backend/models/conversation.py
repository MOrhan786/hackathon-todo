from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func
from uuid import UUID, uuid4
from datetime import datetime


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session between user and assistant.

    Attributes:
        id: Unique identifier for the conversation
        user_id: ID of the user who owns the conversation
        created_at: Timestamp when the conversation was created
        updated_at: Timestamp when the conversation was last updated
    """
    __tablename__ = "conversations"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )
    user_id: str = Field(index=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
