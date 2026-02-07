"""
Quick test script to verify Phase 3 implementation.
"""

import sys
from sqlmodel import Session, select
from core.db import engine, create_db_and_tables
from models.conversation import Conversation
from models.message import Message, MessageRole
from models.task import Task
from uuid import uuid4

def test_database_setup():
    """Test that all tables are created."""
    print("Testing database setup...")

    try:
        # Create tables
        create_db_and_tables()
        print("✓ Database tables created successfully")

        # Test creating a conversation
        with Session(engine) as session:
            test_user_id = "test-user-123"

            # Create a conversation
            conv = Conversation(user_id=test_user_id)
            session.add(conv)
            session.commit()
            session.refresh(conv)
            print(f"✓ Created conversation: {conv.id}")

            # Create a message
            msg = Message(
                conversation_id=conv.id,
                user_id=test_user_id,
                role=MessageRole.USER,
                content="Test message"
            )
            session.add(msg)
            session.commit()
            session.refresh(msg)
            print(f"✓ Created message: {msg.id}")

            # Query back
            stmt = select(Message).where(Message.conversation_id == conv.id)
            messages = session.exec(stmt).all()
            print(f"✓ Retrieved {len(messages)} message(s)")

            # Cleanup (delete message first due to foreign key constraint)
            session.delete(msg)
            session.commit()
            session.delete(conv)
            session.commit()
            print("✓ Cleaned up test data")

        print("\n✅ All database tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tools_import():
    """Test that tools can be imported."""
    print("\nTesting tools import...")

    try:
        from tools.task_tools import TASK_TOOLS, TaskToolExecutor
        print(f"✓ Found {len(TASK_TOOLS)} task management tools:")
        for tool in TASK_TOOLS:
            print(f"  - {tool['function']['name']}")

        print("\n✅ All tool tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Tools test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chatbot_service():
    """Test that chatbot service can be imported."""
    print("\nTesting chatbot service...")

    try:
        from services.chatbot_service import ChatbotService
        print("✓ ChatbotService imported successfully")

        from services.conversation_service import ConversationService
        print("✓ ConversationService imported successfully")

        print("\n✅ All service tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3 Implementation Tests")
    print("=" * 60)

    results = []
    results.append(("Database Setup", test_database_setup()))
    results.append(("Tools Import", test_tools_import()))
    results.append(("Services Import", test_chatbot_service()))

    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")

    all_passed = all(passed for _, passed in results)

    if all_passed:
        print("\n🎉 All tests passed! Phase 3 implementation is ready.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        sys.exit(1)
