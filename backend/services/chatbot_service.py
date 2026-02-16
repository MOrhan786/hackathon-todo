"""
Chatbot service using OpenAI for natural language understanding.

Integrates with OpenAI's chat completion API and function calling
to provide intelligent task management assistance.
"""

from typing import Dict, List, Optional
from uuid import UUID
from sqlmodel import Session, select
from openai import OpenAI
from core.config import settings
from models.message import Message, MessageRole
from tools.task_tools import TASK_TOOLS, TaskToolExecutor
import json
import logging

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# System prompt for the AI assistant
SYSTEM_PROMPT = """You are a helpful task management assistant. You help users:
- Create tasks with title, description, priority, and due dates
- List and filter their tasks
- Update task details (title, description, priority, status, due date)
- Complete tasks
- Delete tasks

Be concise, friendly, and helpful. When users ask to create, list, update, complete, or delete tasks, use the provided tools to perform these actions. Always confirm actions and provide clear feedback about what was done.

When interpreting dates:
- "today" = current date
- "tomorrow" = current date + 1 day
- "next week" = current date + 7 days
- Convert relative dates to ISO format (YYYY-MM-DD)

Priority levels: low, medium (default), high, urgent
Status levels: pending (default), in_progress, completed"""


class ChatbotService:
    """Service for handling AI-powered chatbot interactions."""

    @staticmethod
    def get_conversation_history(
        session: Session,
        conversation_id: UUID,
        user_id: str,
        limit: int = 50
    ) -> List[Dict]:
        """
        Fetch conversation history for context.

        Args:
            session: Database session
            conversation_id: UUID of the conversation
            user_id: User ID for authorization
            limit: Maximum number of messages to retrieve

        Returns:
            List of message dictionaries with role and content
        """
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .where(Message.user_id == user_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )

        messages = session.exec(statement).all()

        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]

    @staticmethod
    def handle_chat_message(
        session: Session,
        user_id: str,
        user_message: str,
        conversation_id: UUID
    ) -> Dict:
        """
        Handle user message with AI agent.

        Args:
            session: Database session
            user_id: User ID
            user_message: User's message text
            conversation_id: UUID of the conversation

        Returns:
            Dictionary with assistant response and conversation_id
        """
        try:
            # Save user message to database
            user_msg = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=MessageRole.USER,
                content=user_message
            )
            session.add(user_msg)
            session.commit()

            # Fetch conversation history
            history = ChatbotService.get_conversation_history(
                session, conversation_id, user_id
            )

            # Prepare messages for OpenAI (system + history)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(history)

            # Call OpenAI with function calling
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=TASK_TOOLS,
                tool_choice="auto",
                timeout=30
            )

            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls

            # If the model wants to call tools
            if tool_calls:
                # Execute each tool call
                tool_executor = TaskToolExecutor(session, user_id)
                tool_results = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    logger.info(f"Executing tool: {function_name} with args: {function_args}")

                    # Execute the tool
                    result = tool_executor.execute_tool(function_name, function_args)
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })

                # Add assistant message with tool calls to context
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in tool_calls
                    ]
                })

                # Add tool results to context
                messages.extend(tool_results)

                # Get final response from OpenAI after tool execution
                final_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    timeout=30
                )

                assistant_content = final_response.choices[0].message.content

            else:
                # No tool calls, use the response directly
                assistant_content = assistant_message.content

            # Save assistant message to database
            assistant_msg = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=assistant_content
            )
            session.add(assistant_msg)
            session.commit()

            return {
                "message": assistant_content,
                "conversation_id": str(conversation_id)
            }

        except Exception as e:
            logger.error(f"Error in chat message handling: {e}", exc_info=True)

            # Provide specific error messages based on error type
            error_type = type(e).__name__
            if "RateLimitError" in error_type or "insufficient_quota" in str(e).lower():
                error_message = "⚠️ OpenAI API quota exceeded. Please check your API billing at https://platform.openai.com/account/billing or use a different API key."
            elif "AuthenticationError" in error_type:
                error_message = "⚠️ OpenAI API authentication failed. Please check your API key configuration."
            elif "InvalidRequestError" in error_type:
                error_message = "⚠️ Invalid request to OpenAI API. The chatbot configuration may need adjustment."
            else:
                error_message = f"I apologize, but I'm having trouble processing your request right now. Error: {error_type}. Please try again or contact support."

            # Try to save error message to conversation
            try:
                error_msg = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role=MessageRole.ASSISTANT,
                    content=error_message
                )
                session.add(error_msg)
                session.commit()
            except Exception as save_error:
                logger.error(f"Failed to save error message: {save_error}")

            return {
                "message": error_message,
                "conversation_id": str(conversation_id)
            }
