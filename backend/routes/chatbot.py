"""
Chatbot API routes for natural language task management.

Provides endpoints for AI-powered chat interactions.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime
from core.db import get_session
from core.security import get_current_user
from schemas.chatbot import ChatRequest, ChatResponse
from services.chatbot_service import ChatbotService
from services.conversation_service import ConversationService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chatbot"])


@router.post("/message", response_model=ChatResponse)
def send_message(
    chat_request: ChatRequest,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Send a message to the AI chatbot and get a response.

    Args:
        chat_request: Chat request containing user message and optional conversation_id
        current_user_id: Authenticated user ID from JWT token
        session: Database session

    Returns:
        ChatResponse: AI chatbot's response with conversation_id for context tracking
    """
    try:
        # Get or create conversation
        conversation = ConversationService.get_or_create_conversation(
            session,
            current_user_id,
            chat_request.conversation_id
        )

        logger.info(f"Processing message for user {current_user_id}, conversation {conversation.id}")

        # Handle message with AI agent
        result = ChatbotService.handle_chat_message(
            session,
            current_user_id,
            chat_request.message,
            conversation.id
        )

        return ChatResponse(
            message=result["message"],
            conversation_id=conversation.id,
            intent=None,  # No longer using intent-based system
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )
