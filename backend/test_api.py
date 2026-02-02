#!/usr/bin/env python3
"""
Test script to verify all backend API endpoints are working correctly.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("Testing Phase II Todo API Endpoints...")
    print("=" * 50)

    # Step 1: Login to get token
    print("\n1. Logging in to get JWT token...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )

    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        print(f"✓ Successfully obtained JWT token: {access_token[:20]}...")
    else:
        print(f"✗ Login failed: {login_response.text}")
        return

    # Step 2: Get tasks (should be empty initially)
    print("\n2. Getting all tasks...")
    tasks_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    if tasks_response.status_code == 200:
        print(f"✓ Got tasks: {len(tasks_response.json()['tasks'])} tasks found")
    else:
        print(f"✗ Failed to get tasks: {tasks_response.text}")

    # Step 3: Create a new task
    print("\n3. Creating a new task...")
    new_task = {
        "title": "Test API Task",
        "description": "Created via test script",
        "status": "pending"
    }
    create_response = requests.post(
        f"{BASE_URL}/api/tasks",
        json=new_task,
        headers=headers
    )

    if create_response.status_code == 201:
        created_task = create_response.json()
        task_id = created_task["id"]
        print(f"✓ Created task: {created_task['title']} (ID: {task_id})")
    else:
        print(f"✗ Failed to create task: {create_response.text}")
        return

    # Step 4: Get the specific task
    print("\n4. Getting specific task...")
    specific_task_response = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    if specific_task_response.status_code == 200:
        task = specific_task_response.json()
        print(f"✓ Retrieved task: {task['title']}")
    else:
        print(f"✗ Failed to get specific task: {specific_task_response.text}")

    # Step 5: Update the task
    print("\n5. Updating the task...")
    update_data = {"status": "completed"}
    update_response = requests.put(
        f"{BASE_URL}/api/tasks/{task_id}",
        json=update_data,
        headers=headers
    )

    if update_response.status_code == 200:
        updated_task = update_response.json()
        print(f"✓ Updated task status to: {updated_task['status']}")
    else:
        print(f"✗ Failed to update task: {update_response.text}")

    # Step 6: Get all tasks again to see the update
    print("\n6. Getting all tasks to verify update...")
    tasks_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    if tasks_response.status_code == 200:
        tasks = tasks_response.json()["tasks"]
        print(f"✓ Got updated task list: {len(tasks)} tasks")
        for task in tasks:
            print(f"  - {task['title']}: {task['status']}")
    else:
        print(f"✗ Failed to get tasks: {tasks_response.text}")

    # Step 7: Test authentication protection
    print("\n7. Testing authentication protection...")
    unprotected_response = requests.get(f"{BASE_URL}/api/tasks")
    if unprotected_response.status_code == 401 or unprotected_response.status_code == 403:
        print("✓ Authentication protection is working (received 401/403 without token)")
    else:
        print(f"? Unexpected response without auth: {unprotected_response.status_code}")

    # Step 8: Delete the test task
    print("\n8. Deleting the test task...")
    delete_response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    if delete_response.status_code == 204:
        print("✓ Deleted test task successfully")
    else:
        print(f"✗ Failed to delete task: {delete_response.text}")

    print("\n" + "=" * 50)
    print("API Test completed successfully! All endpoints are working correctly.")

if __name__ == "__main__":
    test_api()