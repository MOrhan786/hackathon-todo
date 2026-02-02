#!/usr/bin/env python3
"""
Test script to verify the authentication fixes work correctly.
"""

def test_imports():
    """Test that all necessary modules can be imported without errors."""
    print("Testing imports...")

    try:
        from routes.tasks import router
        print("✓ Successfully imported tasks router")
    except Exception as e:
        print(f"✗ Failed to import tasks router: {e}")
        return False

    try:
        from src.middleware.auth import get_current_user
        print("✓ Successfully imported get_current_user")
    except Exception as e:
        print(f"✗ Failed to import get_current_user: {e}")
        return False

    try:
        from models.user import User
        print("✓ Successfully imported User model")
    except Exception as e:
        print(f"✗ Failed to import User model: {e}")
        return False

    try:
        from models.task import Task
        print("✓ Successfully imported Task model")
    except Exception as e:
        print(f"✗ Failed to import Task model: {e}")
        return False

    try:
        from core.db import get_session
        print("✓ Successfully imported get_session")
    except Exception as e:
        print(f"✗ Failed to import get_session: {e}")
        return False

    try:
        from src.utils.auth import verify_token, create_access_token
        print("✓ Successfully imported auth utilities")
    except Exception as e:
        print(f"✗ Failed to import auth utilities: {e}")
        return False

    print("All imports successful!")
    return True

def test_basic_auth_functionality():
    """Test basic authentication functionality."""
    print("\nTesting basic auth functionality...")

    try:
        from src.utils.auth import create_access_token
        from core.config import settings
        import uuid

        # Create a test token
        test_user_id = str(uuid.uuid4())
        token_data = {"sub": test_user_id}
        token = create_access_token(data=token_data)

        print(f"✓ Successfully created token: {token[:20]}...")

        # Test token verification
        from src.utils.auth import verify_token
        payload = verify_token(token)

        if payload and payload.get("sub") == test_user_id:
            print("✓ Token verification successful")
        else:
            print("✗ Token verification failed")
            return False

    except Exception as e:
        print(f"✗ Failed auth functionality test: {e}")
        return False

    print("Basic auth functionality test passed!")
    return True

if __name__ == "__main__":
    print("Running authentication fix tests...\n")

    success = True
    success &= test_imports()
    success &= test_basic_auth_functionality()

    if success:
        print("\n🎉 All tests passed! Authentication fixes appear to be working correctly.")
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        exit(1)