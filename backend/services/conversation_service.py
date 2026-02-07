"""
Conversation service for managing chat conversations.

Provides CRUD operations for conversations with user isolation.
"""

from sqlmodel import Session, select
from uuid import UUID
from typing import Optional
from models.conversation import Conversation


class ConversationService:
    """
    Service class for handling conversation-related operations.

    Provides operations for creating and retrieving conversations.
    """

    @staticmethod
    def get_or_create_conversation(
        session: Session,
        user_id: str,
        conversation_id: Optional[UUID] = None
    ) -> Conversation:
        """
        Get an existing conversation or create a new one.

        Args:
            session: Database session
            user_id: ID of the user
            conversation_id: Optional UUID of existing conversation

        Returns:
            Conversation object (existing or newly created)
        """
        # Try to get existing conversation if ID provided
        if conversation_id:
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            conv = session.exec(statement).first()
            if conv:
                return conv

        # Create new conversation
        conv = Conversation(user_id=user_id)
        session.add(conv)
        session.commit()
        session.refresh(conv)
        return conv

    @staticmethod
    def get_conversation(
        session: Session,
        conversation_id: UUID,
        user_id: str
    ) -> Optional[Conversation]:
        """
        Get a specific conversation if it belongs to the user.

        Args:
            session: Database session
            conversation_id: UUID of the conversation
            user_id: ID of the user

        Returns:
            Conversation object if found and authorized, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()
