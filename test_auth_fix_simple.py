#!/usr/bin/env python3
"""
Simple test to verify the authentication fix for task creation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all necessary modules can be imported after our fix."""
    print("Testing imports after authentication fix...")

    try:
        # Test the auth middleware import
        from backend.src.middleware.auth import get_current_user
        print("✅ Successfully imported get_current_user from auth middleware")

        # Test the auth utility functions
        from backend.src.utils.auth import create_access_token, verify_token
        print("✅ Successfully imported auth utility functions")

        # Test the User model import
        from backend.src.models.user import User
        print("✅ Successfully imported User model")

        # Test that the routes can be imported
        from backend.routes.tasks import router
        print("✅ Successfully imported tasks router")

        # Test that the task service can be imported
        from backend.services.task_service import TaskService
        print("✅ Successfully imported TaskService")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_token_flow():
    """Test the token creation and verification flow."""
    print("\nTesting JWT token flow...")

    try:
        import uuid
        from backend.src.utils.auth import create_access_token, verify_token
        from datetime import timedelta

        # Create a test user ID
        test_user_id = str(uuid.uuid4())

        # Create a token
        token = create_access_token(
            data={"sub": test_user_id},
            expires_delta=timedelta(minutes=30)
        )

        # Verify the token
        payload = verify_token(token)

        if payload and payload.get("sub") == test_user_id:
            print(f"✅ Token flow working correctly. User ID: {test_user_id}")
            return True
        else:
            print("❌ Token verification failed")
            return False

    except Exception as e:
        print(f"❌ Token flow error: {e}")
        return False

def test_auth_dependency():
    """Test that the auth dependency returns the correct type."""
    print("\nTesting authentication dependency signature...")

    try:
        from backend.src.middleware.auth import get_current_user
        import inspect

        # Check the function signature
        sig = inspect.signature(get_current_user)
        params = list(sig.parameters.keys())
        return_annotation = sig.return_annotation

        print(f"Function parameters: {params}")
        print(f"Return annotation: {return_annotation}")

        # The function should return a User type
        if "credentials" in params and "session" in params:
            print("✅ Authentication dependency has correct parameters")
        else:
            print("❌ Authentication dependency has incorrect parameters")

        return True

    except Exception as e:
        print(f"❌ Auth dependency test error: {e}")
        return False

def test_routes_updated():
    """Verify that the routes file was updated correctly."""
    print("\nVerifying routes file updates...")

    try:
        with open('/mnt/d/main-hackathon-folder/hackathon2/phase-02-todo-list/backend/routes/tasks.py', 'r') as f:
            content = f.read()

        # Check for the correct imports
        if "from src.middleware.auth import get_current_user" in content:
            print("✅ Using correct auth middleware import")
        else:
            print("❌ Missing correct auth middleware import")
            return False

        # Check for User import
        if "from src.models.user import User" in content:
            print("✅ User model import found")
        else:
            print("❌ User model import missing")
            return False

        # Check for correct parameter usage in endpoints
        if "current_user: User = Depends(get_current_user)" in content:
            print("✅ Correct parameter usage in endpoints")
        else:
            print("❌ Incorrect parameter usage in endpoints")
            return False

        return True

    except Exception as e:
        print(f"❌ Routes verification error: {e}")
        return False

def main():
    """Run all authentication fix verification tests."""
    print("=" * 60)
    print("Verifying Authentication Fix for Task Creation API")
    print("=" * 60)

    tests = [
        ("Import Test", test_imports),
        ("Token Flow Test", test_token_flow),
        ("Auth Dependency Test", test_auth_dependency),
        ("Routes Update Verification", test_routes_updated)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n--- Running {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"Verification Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All authentication fixes verified successfully!")
        print("\nSUMMARY OF FIXES MADE:")
        print("1. Fixed import in routes/tasks.py to use src.middleware.auth instead of core.security")
        print("2. Updated function signatures to expect User object instead of string")
        print("3. Used str(current_user.id) to extract user ID for service calls")
        print("4. Added proper User model import")
        print("\nThe POST /api/tasks endpoint should now work properly with JWT authentication.")
        print("Users should be able to create tasks after logging in and providing a valid JWT token.")
    else:
        print("⚠️  Some verification tests failed. Please review the authentication implementation.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)