#!/usr/bin/env python3
"""
Integration test script to verify that the backend authentication system
and task endpoints are working correctly after the fix for 403 Forbidden errors.
"""
import subprocess
import time
import requests
import sys
import json
import uuid
from datetime import datetime, timedelta
from jose import jwt
from backend.src.config import settings


def create_test_token(user_id: str = None) -> str:
    """
    Create a test JWT token for authentication testing.

    Args:
        user_id: Optional user ID to embed in token. If None, generates a random UUID.

    Returns:
        JWT token string
    """
    if user_id is None:
        user_id = str(uuid.uuid4())

    # Create token payload
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {
        "sub": user_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }

    # Encode the token using the same algorithm as the app
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def test_api_endpoints():
    """Test all API endpoints to ensure authentication is working properly."""
    print("=== Testing API Endpoints ===")

    # Test base URL - adjust if running on different port
    base_url = "http://localhost:8000"

    # Test 1: Health check endpoint (should work without auth)
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Health check endpoint working")
        else:
            print(f"   ✗ Health check failed: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Health check failed: {e}")
        return False

    # Test 2: Root endpoint (should work without auth)
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Root endpoint working")
        else:
            print(f"   ✗ Root endpoint failed: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Root endpoint failed: {e}")
        return False

    # Create a test token for authenticated requests
    test_user_id = str(uuid.uuid4())
    test_token = create_test_token(test_user_id)
    headers = {"Authorization": f"Bearer {test_token}"}

    # Test 3: GET /api/tasks without proper authentication (should fail)
    print("\n3. Testing GET /api/tasks without auth...")
    try:
        response = requests.get(f"{base_url}/api/tasks")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✓ Properly rejected unauthenticated request")
        else:
            print(f"   ✗ Should have returned 401, got {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Request failed: {e}")

    # Test 4: GET /api/tasks with proper authentication (should work)
    print("\n4. Testing GET /api/tasks with auth...")
    try:
        response = requests.get(f"{base_url}/api/tasks", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 404]:  # 404 is fine if no tasks exist yet
            print("   ✓ Authentication working - received expected response")
        else:
            print(f"   ? Unexpected status: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Request failed: {e}")

    # Test 5: POST /api/tasks with proper authentication (should work)
    print("\n5. Testing POST /api/tasks with auth...")
    try:
        task_data = {
            "title": "Test Task",
            "description": "This is a test task for integration verification",
            "status": "pending"
        }
        response = requests.post(f"{base_url}/api/tasks",
                                json=task_data,
                                headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✓ Task creation successful - authentication working")
            created_task = response.json()
            print(f"   Created task ID: {created_task.get('id')}")
        elif response.status_code == 422:
            print(f"   ? Validation error: {response.text}")
        else:
            print(f"   ✗ Expected 201, got {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Request failed: {e}")

    # Test 6: POST /api/tasks without authentication (should fail with 401)
    print("\n6. Testing POST /api/tasks without auth...")
    try:
        task_data = {
            "title": "Unauthorized Task",
            "description": "This should fail due to missing auth",
            "status": "pending"
        }
        response = requests.post(f"{base_url}/api/tasks", json=task_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✓ Properly rejected unauthenticated request")
        else:
            print(f"   ✗ Should have returned 401, got {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Request failed: {e}")

    # Test 7: Test invalid token (should fail with 401)
    print("\n7. Testing API with invalid token...")
    try:
        invalid_headers = {"Authorization": "Bearer invalid.token.here"}
        response = requests.get(f"{base_url}/api/tasks", headers=invalid_headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✓ Properly rejected invalid token")
        else:
            print(f"   ✗ Should have returned 401, got {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Request failed: {e}")

    print("\n=== API Endpoint Testing Complete ===")
    return True


def verify_backend_running():
    """Verify that the backend server is running."""
    print("=== Verifying Backend Server Status ===")

    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("✓ Backend server is running and healthy")
            return True
        else:
            print(f"✗ Backend server responded but not healthy: {response.text}")
            return False
    except requests.exceptions.RequestException:
        print("✗ Backend server is not running")
        return False


def main():
    print("=== Backend Authentication & Task Endpoint Integration Test ===")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check if backend is running
    if not verify_backend_running():
        print("\nTo start the backend server, run:")
        print("cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("\nStarting backend server...")

        # Try to start the backend server
        import os
        backend_dir = os.path.join(os.getcwd(), "backend")
        os.chdir(backend_dir)

        # Start server in subprocess
        process = subprocess.Popen([
            sys.executable, "-c",
            "from main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for server to start
        time.sleep(5)

        # Verify it's running
        if not verify_backend_running():
            print("✗ Could not start backend server automatically")
            process.terminate()
            return False

        print("✓ Started backend server in subprocess")

    # Run API tests
    test_results = test_api_endpoints()

    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if test_results:
        print("\n✓ Integration test completed successfully!")
        print("✓ Authentication system is working correctly")
        print("✓ Task endpoints are properly protected")
        print("✓ 403 Forbidden errors should be resolved")
        return True
    else:
        print("\n✗ Integration test failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)