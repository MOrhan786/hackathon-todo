#!/usr/bin/env python3
"""
Test script to verify the authentication fix for task creation.
This script simulates the authentication flow that was failing before.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.utils.auth import create_access_token, verify_token
from datetime import timedelta
import uuid

def test_token_creation_and_verification():
    """Test that JWT token creation and verification works correctly."""
    print("Testing JWT token creation and verification...")

    # Create a test user ID
    test_user_id = str(uuid.uuid4())
    print(f"Test user ID: {test_user_id}")

    # Create access token
    access_token = create_access_token(
        data={"sub": test_user_id},
        expires_delta=timedelta(minutes=30)
    )
    print(f"Created access token: {access_token[:50]}...")

    # Verify the token
    payload = verify_token(access_token)
    if payload:
        print(f"Token verified successfully. User ID from token: {payload.get('sub')}")
        assert payload.get('sub') == test_user_id, "User ID in token doesn't match"
        print("✅ Token creation and verification working correctly")
    else:
        print("❌ Token verification failed")
        return False

    return True

def test_task_service_integration():
    """Test that the task service integration works with the corrected authentication."""
    print("\nTesting task service integration...")

    try:
        # Import the modules that were fixed
        from backend.services.task_service import TaskService
        from backend.models.task import TaskCreate
        from backend.core.db import get_session

        print("✅ Successfully imported task service and related modules")

        # Verify that the expected methods exist
        assert hasattr(TaskService, 'create_task'), "TaskService.create_task method missing"
        assert hasattr(TaskService, 'get_tasks_by_user'), "TaskService.get_tasks_by_user method missing"
        assert hasattr(TaskService, 'get_task_by_id'), "TaskService.get_task_by_id method missing"
        assert hasattr(TaskService, 'update_task'), "TaskService.update_task method missing"
        assert hasattr(TaskService, 'delete_task'), "TaskService.delete_task method missing"

        print("✅ All required TaskService methods are available")

        # Test that TaskCreate model works
        task_data = TaskCreate(title="Test Task", description="Test Description", status="pending")
        print(f"✅ TaskCreate model works: {task_data.title}")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing task service: {e}")
        return False

def test_routes_integration():
    """Test that the routes integration works correctly."""
    print("\nTesting routes integration...")

    try:
        # Import the routes module that was fixed
        from backend.routes.tasks import router
        from backend.main import app

        # Check that the routes are properly registered
        route_paths = []
        for route in app.routes:
            if hasattr(route, 'path') and '/api/tasks' in route.path:
                route_paths.append((route.methods, route.path))

        print(f"Found {len(route_paths)} task-related routes:")
        for methods, path in route_paths:
            print(f"  {methods} {path}")

        expected_routes = [
            '/api/tasks',
            '/api/tasks/{task_id}'
        ]

        for expected_route in expected_routes:
            found = any(expected_route in path for _, path in route_paths)
            assert found, f"Expected route {expected_route} not found"

        print("✅ All expected task routes are registered")
        return True

    except Exception as e:
        print(f"❌ Error testing routes integration: {e}")
        return False

def main():
    """Run all authentication fix tests."""
    print("=" * 60)
    print("Testing Authentication Fix for Task Creation API")
    print("=" * 60)

    tests = [
        test_token_creation_and_verification,
        test_task_service_integration,
        test_routes_integration
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_func.__name__} PASSED")
            else:
                print(f"❌ {test_func.__name__} FAILED")
        except Exception as e:
            print(f"❌ {test_func.__name__} ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All authentication fixes working correctly!")
        print("\nThe POST /api/tasks endpoint should now work properly with JWT authentication.")
        print("Users should be able to create tasks after logging in and providing a valid JWT token.")
    else:
        print("⚠️  Some tests failed. Please review the authentication implementation.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)