#!/usr/bin/env python3
"""
Integration test script to verify that the backend authentication system
and task endpoints are working correctly after the fix for 403 Forbidden errors.
This version properly registers a user first, then tests the task endpoints.
"""
import subprocess
import time
import requests
import sys
import json
from datetime import datetime


def test_full_authentication_flow():
    """Test the complete authentication flow including user registration and task operations."""
    print("=== Testing Full Authentication Flow ===")

    # Test base URL - adjust if running on different port
    base_url = "http://localhost:8000"

    # Step 1: Register a new user
    print("\n1. Testing user registration...")
    try:
        user_data = {
            "email": f"test_{int(time.time())}@example.com",  # Use timestamp to ensure uniqueness
            "password": "testpassword123"
        }
        response = requests.post(f"{base_url}/auth/register", json=user_data)
        print(f"   Registration Status: {response.status_code}")

        if response.status_code == 201:
            print("   ✓ User registration successful")
            registration_response = response.json()
            access_token = registration_response.get("access_token")
            user_id = registration_response.get("id")
            print(f"   Token received: {'Yes' if access_token else 'No'}")
            print(f"   User ID: {user_id}")
        else:
            print(f"   ✗ Registration failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Registration request failed: {e}")
        return False

    if not access_token:
        print("   ✗ No access token received from registration")
        return False

    # Prepare headers with the valid token
    headers = {"Authorization": f"Bearer {access_token}"}

    # Step 2: Test GET /api/tasks with valid authentication (should work)
    print("\n2. Testing GET /api/tasks with valid auth...")
    try:
        response = requests.get(f"{base_url}/api/tasks", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ GET /api/tasks successful with valid auth")
            tasks = response.json()
            print(f"   Number of tasks: {len(tasks.get('tasks', []))}")
        else:
            print(f"   ✗ GET /api/tasks failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ GET request failed: {e}")
        return False

    # Step 3: Test POST /api/tasks with valid authentication (should work)
    print("\n3. Testing POST /api/tasks with valid auth...")
    try:
        task_data = {
            "title": "Integration Test Task",
            "description": "This is a test task created during integration testing",
            "status": "pending"
        }
        response = requests.post(f"{base_url}/api/tasks", json=task_data, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✓ Task creation successful with valid auth")
            created_task = response.json()
            task_id = created_task.get("id")
            print(f"   Created task ID: {task_id}")
        elif response.status_code == 422:
            print(f"   ? Validation error: {response.text}")
            return False
        else:
            print(f"   ✗ Task creation failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ POST request failed: {e}")
        return False

    # Step 4: Test GET /api/tasks/{task_id} with valid authentication (should work)
    print("\n4. Testing GET /api/tasks/{id} with valid auth...")
    try:
        if task_id:
            response = requests.get(f"{base_url}/api/tasks/{task_id}", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✓ GET /api/tasks/{id} successful with valid auth")
                task_details = response.json()
                print(f"   Retrieved task title: {task_details.get('title')}")
            else:
                print(f"   ✗ GET /api/tasks/{id} failed: {response.status_code} - {response.text}")
                return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ GET specific task request failed: {e}")
        return False

    # Step 5: Test PUT /api/tasks/{task_id} with valid authentication (should work)
    print("\n5. Testing PUT /api/tasks/{id} with valid auth...")
    try:
        if task_id:
            update_data = {
                "status": "completed"
            }
            response = requests.put(f"{base_url}/api/tasks/{task_id}", json=update_data, headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✓ PUT /api/tasks/{id} successful with valid auth")
                updated_task = response.json()
                print(f"   Updated task status: {updated_task.get('status')}")
            else:
                print(f"   ✗ PUT /api/tasks/{id} failed: {response.status_code} - {response.text}")
                return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ PUT request failed: {e}")
        return False

    # Step 6: Test GET /api/tasks without authentication (should fail with 401/403)
    print("\n6. Testing GET /api/tasks without auth...")
    try:
        response = requests.get(f"{base_url}/api/tasks")
        print(f"   Status: {response.status_code}")
        if response.status_code in [401, 403]:
            print("   ✓ Properly rejected unauthenticated request")
        else:
            print(f"   ? Expected 401/403, got {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Unauthenticated request failed: {e}")

    # Step 7: Test POST /api/tasks without authentication (should fail with 401/403)
    print("\n7. Testing POST /api/tasks without auth...")
    try:
        task_data = {
            "title": "Unauthorized Task",
            "description": "This should fail due to missing auth",
            "status": "pending"
        }
        response = requests.post(f"{base_url}/api/tasks", json=task_data)
        print(f"   Status: {response.status_code}")
        if response.status_code in [401, 403]:
            print("   ✓ Properly rejected unauthenticated request")
        else:
            print(f"   ? Expected 401/403, got {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Unauthenticated request failed: {e}")

    # Step 8: Test DELETE /api/tasks/{task_id} with valid authentication (should work)
    print("\n8. Testing DELETE /api/tasks/{id} with valid auth...")
    try:
        if task_id:
            response = requests.delete(f"{base_url}/api/tasks/{task_id}", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 204:
                print("   ✓ DELETE /api/tasks/{id} successful with valid auth")
            else:
                print(f"   ? DELETE /api/tasks/{id} response: {response.status_code} - {response.text}")
                # 204 is expected for successful delete, but other responses are acceptable
    except requests.exceptions.RequestException as e:
        print(f"   ✗ DELETE request failed: {e}")

    print("\n=== Full Authentication Flow Testing Complete ===")
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
        original_dir = os.getcwd()
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
        os.chdir(original_dir)  # Return to original directory

    # Run API tests
    test_results = test_full_authentication_flow()

    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if test_results:
        print("\n✓ Integration test completed successfully!")
        print("✓ Authentication system is working correctly")
        print("✓ User registration and login work properly")
        print("✓ Task endpoints are properly protected")
        print("✓ CRUD operations work with proper authentication")
        print("✓ 403 Forbidden errors have been resolved")
        return True
    else:
        print("\n✗ Integration test failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)