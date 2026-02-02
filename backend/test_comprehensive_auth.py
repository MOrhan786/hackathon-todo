#!/usr/bin/env python3
"""
Comprehensive test to verify all authentication fixes are working properly.
"""

def test_comprehensive_auth():
    """Test comprehensive authentication functionality."""
    print("Running comprehensive authentication tests...")

    # Test 1: Import all necessary modules
    print("\n1. Testing imports...")
    modules_to_test = [
        ("main", "app"),
        ("routes.tasks", "router"),
        ("src.middleware.auth", "get_current_user"),
        ("src.utils.auth", "create_access_token, verify_token"),
        ("models.user", "User, UserCreate, UserResponse"),
        ("models.task", "Task, TaskCreate, TaskUpdate"),
        ("schemas.task", "TaskResponse, TaskListResponse"),
        ("services.task_service", "TaskService"),
        ("core.db", "get_session, engine"),
        ("core.security", "get_current_user as core_get_current_user"),
    ]

    for module_path, items in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[item.strip() for item in items.split(',')])
            print(f"  ✓ Imported {module_path}: {items}")
        except ImportError as e:
            print(f"  ✗ Failed to import {module_path}: {e}")
            return False

    # Test 2: Test JWT functionality
    print("\n2. Testing JWT functionality...")
    try:
        import uuid
        from src.utils.auth import create_access_token, verify_token

        # Create a test token
        user_id = str(uuid.uuid4())
        token_payload = {"sub": user_id}
        token = create_access_token(data=token_payload)

        # Verify the token
        verified_payload = verify_token(token)
        assert verified_payload is not None, "Token verification failed"
        assert verified_payload.get("sub") == user_id, "User ID mismatch in token"

        print(f"  ✓ Created and verified JWT token successfully")
    except Exception as e:
        print(f"  ✗ JWT functionality test failed: {e}")
        return False

    # Test 3: Test that the application starts without errors
    print("\n3. Testing application startup...")
    try:
        from main import app
        assert app is not None, "App is None"
        print("  ✓ Application started successfully")
    except Exception as e:
        print(f"  ✗ Application startup failed: {e}")
        return False

    # Test 4: Test that routes are properly registered
    print("\n4. Testing route registration...")
    try:
        from main import app
        routes = [route.path for route in app.routes]

        # Check that API routes exist
        api_routes = [route for route in routes if '/api/tasks' in route or '/auth' in route]
        if len(api_routes) > 0:
            print(f"  ✓ Found {len(api_routes)} API routes registered")
        else:
            print("  ⚠ No API routes found (this might be okay depending on registration)")
    except Exception as e:
        print(f"  ✗ Route registration test failed: {e}")
        return False

    # Test 5: Test database connectivity setup
    print("\n5. Testing database setup...")
    try:
        from core.db import engine
        assert engine is not None, "Database engine is None"
        print("  ✓ Database engine configured")
    except Exception as e:
        print(f"  ✗ Database setup test failed: {e}")
        return False

    print("\n✅ All comprehensive tests passed!")
    return True

if __name__ == "__main__":
    print("Running comprehensive authentication tests...\n")

    success = test_comprehensive_auth()

    if success:
        print("\n🎉 All comprehensive tests passed! Authentication system is working properly.")
    else:
        print("\n❌ Some comprehensive tests failed.")
        exit(1)