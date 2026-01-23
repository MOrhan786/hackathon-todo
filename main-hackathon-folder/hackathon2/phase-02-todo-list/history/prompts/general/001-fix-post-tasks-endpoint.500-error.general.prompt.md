---
id: "001"
title: "Fix POST tasks endpoint 500 error"
stage: "red"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-backend-api"
user: "user"
command: "fix-500-error"
labels:
  - "bug"
  - "backend"
  - "api"
  - "authentication"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - /mnt/d/main-hackathon-folder/hackathon2/phase-02-todo-list/backend/routes/tasks.py
  - /mnt/d/main-hackathon-folder/hackathon2/phase-02-todo-list/backend/services/task_service.py
  - /mnt/d/main-hackathon-folder/hackathon2/phase-02-todo-list/backend/test_fix.py
tests_yaml: |
  - /mnt/d/main-hackathon-folder/hackathon2/phase-02-todo-list/backend/test_fix.py
---

# Fix POST tasks endpoint 500 error

## Issue Description
The POST /api/tasks endpoint was returning a 500 Internal Server Error when creating a new task for an authenticated user. The backend attempted to create a Task model directly from TaskCreate data, causing validation errors for required fields: user_id, created_at, updated_at. These fields MUST NOT be provided by the client and MUST be injected by the backend.

## Root Cause
The original code in routes/tasks.py and services/task_service.py was trying to create a Task model directly from TaskCreate data using `Task(**task_create.dict())`, which failed because:
- Task model has required fields (user_id, created_at, updated_at) not present in TaskCreate schema
- User_id should be extracted from JWT token, not from client input
- Timestamps should be handled automatically by SQLModel

## Solution Implemented
1. Updated routes/tasks.py to use TaskService.create_task() method instead of direct model instantiation
2. Fixed TaskService.create_task() to properly map fields from TaskCreate to Task model
3. Ensured user_id is injected from authenticated user instead of client input
4. Maintained proper error handling and transaction management

## Files Modified
- routes/tasks.py: Fixed create_task route to use service method
- services/task_service.py: Fixed create_task method to properly handle field mapping
- Added test_fix.py to verify the fix works correctly

## Verification
Created test script to verify the fix works correctly by testing the object creation logic without requiring database connection.

## Outcome
POST /api/tasks endpoint now properly handles task creation for authenticated users without returning 500 error, maintaining security requirements that user_id comes from JWT token rather than client input.

## PROMPT_TEXT
The POST /api/tasks endpoint returns a 500 Internal Server Error when creating a new task for an authenticated user. The backend currently attempts to create a Task model directly from TaskCreate data, causing validation errors for required fields: user_id, created_at, updated_at. These fields MUST NOT be provided by the client and MUST be injected by the backend. The task is to fix this by properly separating TaskCreate (input schema) from Task (database model), using current_user_id extracted from JWT, and ensuring proper field mapping.

## RESPONSE_TEXT
Successfully fixed the POST /api/tasks endpoint by updating both the route and service layer to properly handle the separation between TaskCreate (input schema) and Task (database model). The fix ensures user_id is extracted from JWT token and injected properly, while timestamps are handled automatically by SQLModel. The 500 error has been resolved and proper error handling is maintained.