#!/usr/bin/env python3
"""
Test script to verify API authentication is working correctly.
This script tests the authentication flow and verifies that users can create tasks after logging in.
"""

import os
import sys
import requests
import json
from datetime import datetime

# Add backend to path
sys.path.insert(0, '/mnt/d/main-hackathon-folder/hackathon2/phase-02-todo-list/backend')

def test_api_endpoints():
    """Test the API endpoints to ensure authentication is working"""

    # API base URL
    BASE_URL = "http://localhost:8000"

    print(f"Testing API endpoints at {BASE_URL}")

    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return

    # Register a test user
    test_email = f"test_{datetime.now().timestamp()}@example.com"
    test_user = {
        "email": test_email,
        "password": "testpassword123"
    }

    print(f"\nRegistering user: {test_email}")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
        print(f"Registration: {response.status_code}")
        if response.status_code == 201:
            auth_data = response.json()
            token = auth_data.get('access_token')
            print(f"Registration successful, got token: {token[:20]}..." if token else "No token received")
        elif response.status_code == 409:
            print("User already exists, continuing with login...")
            # Try to login instead
            login_response = requests.post(f"{BASE_URL}/auth/login", json=test_user)
            if login_response.status_code == 200:
                auth_data = login_response.json()
                token = auth_data.get('access_token')
                print(f"Login successful, got token: {token[:20]}..." if token else "No token received")
            else:
                print(f"Login failed: {login_response.status_code} - {login_response.text}")
                return
        else:
            print(f"Registration failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"Registration/Login failed: {e}")
        return

    # Use the token to create a task
    if 'token' in locals() and token:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        task_data = {
            "title": "Test Task",
            "description": "This is a test task created via API",
            "status": "pending"
        }

        print("\nCreating a task with authentication...")
        try:
            response = requests.post(f"{BASE_URL}/api/tasks", headers=headers, json=task_data)
            print(f"Task creation: {response.status_code}")
            if response.status_code == 201:
                task = response.json()
                print(f"Task created successfully: {task.get('title', 'Unknown')}")
            else:
                print(f"Task creation failed: {response.status_code} - {response.text}")

                # Check if it's an authentication issue
                if response.status_code in [401, 403]:
                    print("Authentication error - check JWT configuration!")

        except Exception as e:
            print(f"Task creation failed: {e}")

    # Test getting tasks
    if 'token' in locals() and token:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        print("\nGetting tasks with authentication...")
        try:
            response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
            print(f"Get tasks: {response.status_code}")
            if response.status_code == 200:
                tasks_data = response.json()
                tasks = tasks_data.get('tasks', [])
                print(f"Retrieved {len(tasks)} tasks")
            else:
                print(f"Get tasks failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Get tasks failed: {e}")

if __name__ == "__main__":
    print("Testing API authentication...")
    test_api_endpoints()
    print("Test completed.")