#!/usr/bin/env python3
"""
Simple test script to verify the backend functionality.
"""
import asyncio
from src.database import get_session_context, create_db_and_tables
from src.services.user_service import UserService
from src.services.todo_service import TodoService
from src.models.user import UserCreate
from src.models.todo import TodoCreate
from src.utils.auth import verify_password, get_password_hash


def test_backend_components():
    """Test the main backend components."""
    print("Testing backend components...")

    # Test password hashing
    password = "test_password_123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed), "Password hashing/verification failed"
    print("✓ Password hashing works")

    # Test database setup
    create_db_and_tables()
    print("✓ Database tables created")

    # Test model creation (just importing to make sure they work)
    user_create = UserCreate(email="test@example.com", password="password123")
    assert user_create.email == "test@example.com"
    print("✓ User model works")

    todo_create = TodoCreate(title="Test Todo", description="A test todo item")
    assert todo_create.title == "Test Todo"
    print("✓ Todo model works")

    print("\nAll backend components tested successfully!")


if __name__ == "__main__":
    test_backend_components()