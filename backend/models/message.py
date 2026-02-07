from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func, Text
from uuid import UUID, uuid4
from datetime import datetime
import enum


class MessageRole(str, enum.Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(SQLModel, table=True):
    """
    Message model representing a single message in a conversation.

    Attributes:
        id: Unique identifier for the message
        conversation_id: Foreign key to the conversation this message belongs to
        user_id: ID of the user who owns this message
        role: Role of the message sender (user/assistant/system)
        content: The actual message content
        created_at: Timestamp when the message was created
    """
    __tablename__ = "messages"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        index=True
    )
    user_id: str = Field(index=True)
    role: MessageRole
    content: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
