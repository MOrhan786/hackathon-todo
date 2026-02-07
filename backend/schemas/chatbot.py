from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import UUID


class ChatIntent(str, Enum):
    """Enumeration of supported chat intents."""
    CREATE_TASK = "create_task"
    LIST_TASKS = "list_tasks"
    UPDATE_TASK = "update_task"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    SET_REMINDER = "set_reminder"
    HELP = "help"
    UNKNOWN = "unknown"


class ChatRequest(BaseModel):
    """Schema for chatbot message request."""
    message: str = Field(..., min_length=1, max_length=1000, description="User's message to the chatbot")
    conversation_id: Optional[UUID] = Field(default=None, description="Optional conversation ID for multi-turn context")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Optional context for conversation")


class ChatResponse(BaseModel):
    """Schema for chatbot message response."""
    message: str = Field(..., description="Chatbot's response message")
    conversation_id: UUID = Field(..., description="Conversation ID for tracking multi-turn context")
    intent: Optional[ChatIntent] = Field(default=None, description="Detected intent from the message (for backward compatibility)")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Response timestamp")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional data (e.g., created task, clarification)")

    class Config:
        use_enum_values = True
