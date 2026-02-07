---
name: fastapi-endpoint-generator
description: "Generate production-ready API endpoints. Creates endpoints that allow the chatbot to interact with task management and other backend services with proper validation and error handling."
version: "1.0.0"
used_by:
  - Full-Stack-Backend
  - Chatbot API Agent
tags:
  - api
  - fastapi
  - endpoints
  - chatbot
---

# FastAPI Endpoint Generator Skill

## Purpose

Generate production-ready FastAPI endpoints with proper validation, error handling, and documentation. This skill creates endpoints that enable chatbot interaction with task management and other backend services.

## Capabilities

### 1. CRUD Endpoint Generation
- Generate Create, Read, Update, Delete endpoints
- Include proper HTTP methods and status codes
- Add request/response validation
- Implement pagination for list endpoints

### 2. Request/Response Models
- Generate Pydantic models for validation
- Create response models with proper typing
- Handle nested objects and relationships
- Support partial updates (PATCH)

### 3. Error Handling
- Implement consistent error responses
- Add proper HTTP status codes
- Include detailed error messages
- Handle validation errors gracefully

### 4. Chatbot API Endpoints
- Create message handling endpoints
- Implement session management
- Support intent/entity extraction results
- Enable task operations via chat

### 5. Documentation
- Generate OpenAPI/Swagger docs
- Add endpoint descriptions
- Document request/response schemas
- Include example payloads

## Code Templates

### Base Router Setup
```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user, TokenPayload

router = APIRouter(prefix="/api/v1", tags=["tasks"])
```

### Request/Response Models
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Create Request
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)

    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "medium",
                "due_date": "2024-12-31T17:00:00Z",
                "tags": ["shopping", "personal"]
            }
        }

# Update Request (Partial)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

# Response Model
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: TaskPriority
    status: TaskStatus
    due_date: Optional[datetime]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

# List Response with Pagination
class TaskListResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    pages: int
```

### CRUD Endpoints
```python
from app.services.task_service import TaskService

task_service = TaskService()

@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user"
)
async def create_task(
    task_data: TaskCreate,
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task with the following information:

    - **title**: Task title (required)
    - **description**: Optional detailed description
    - **priority**: low, medium, high, or urgent
    - **due_date**: Optional due date in ISO format
    - **tags**: Optional list of tag names
    """
    task = await task_service.create_task(
        db=db,
        user_id=user.user_id,
        task_data=task_data
    )
    return task

@router.get(
    "/tasks",
    response_model=TaskListResponse,
    summary="List all tasks",
    description="Get paginated list of tasks for the authenticated user"
)
async def list_tasks(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search in title"),
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve tasks with optional filtering:

    - Filter by **status** (pending, in_progress, completed)
    - Filter by **priority** (low, medium, high, urgent)
    - **Search** in task titles
    - Results are **paginated**
    """
    result = await task_service.list_tasks(
        db=db,
        user_id=user.user_id,
        page=page,
        page_size=page_size,
        status=status,
        priority=priority,
        search=search
    )
    return result

@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    responses={404: {"description": "Task not found"}}
)
async def get_task(
    task_id: int,
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task by ID."""
    task = await task_service.get_task(
        db=db,
        task_id=task_id,
        user_id=user.user_id
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    responses={404: {"description": "Task not found"}}
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task. Only provided fields will be updated.
    """
    task = await task_service.update_task(
        db=db,
        task_id=task_id,
        user_id=user.user_id,
        task_data=task_data
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    responses={404: {"description": "Task not found"}}
)
async def delete_task(
    task_id: int,
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task (soft delete)."""
    success = await task_service.delete_task(
        db=db,
        task_id=task_id,
        user_id=user.user_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

@router.post(
    "/tasks/{task_id}/complete",
    response_model=TaskResponse,
    summary="Mark task as complete"
)
async def complete_task(
    task_id: int,
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a task as completed."""
    task = await task_service.complete_task(
        db=db,
        task_id=task_id,
        user_id=user.user_id
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task
```

### Chatbot API Endpoints
```python
chatbot_router = APIRouter(prefix="/api/v1/chat", tags=["chatbot"])

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None

class ChatMessageResponse(BaseModel):
    response: str
    session_id: str
    intent: Optional[str]
    entities: Optional[dict]
    action_taken: Optional[dict]
    suggestions: List[str] = Field(default_factory=list)

class QuickReply(BaseModel):
    label: str
    payload: str

@chatbot_router.post(
    "/message",
    response_model=ChatMessageResponse,
    summary="Send message to chatbot",
    description="Process a user message and return chatbot response"
)
async def send_message(
    request: ChatMessageRequest,
    user: Optional[TokenPayload] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the chatbot.

    The chatbot can:
    - Create, update, and complete tasks
    - List and search tasks
    - Answer questions about tasks
    - Provide suggestions and reminders

    Authentication is optional but required for task operations.
    """
    response = await chatbot_service.process_message(
        db=db,
        user_id=user.user_id if user else None,
        message=request.message,
        session_id=request.session_id
    )
    return response

@chatbot_router.get(
    "/sessions/{session_id}/history",
    response_model=List[ChatMessageResponse],
    summary="Get chat history"
)
async def get_chat_history(
    session_id: str,
    limit: int = Query(50, ge=1, le=100),
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history for a session."""
    history = await chatbot_service.get_history(
        db=db,
        session_id=session_id,
        user_id=user.user_id,
        limit=limit
    )
    return history

@chatbot_router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="End chat session"
)
async def end_session(
    session_id: str,
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End a chat session."""
    await chatbot_service.end_session(
        db=db,
        session_id=session_id,
        user_id=user.user_id
    )
```

### Error Handling
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class APIError(Exception):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None
    ):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code or "API_ERROR",
                "message": exc.detail
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": errors
            }
        }
    )
```

## Service Layer Pattern
```python
class TaskService:
    """Service layer for task operations."""

    async def create_task(
        self,
        db: Session,
        user_id: int,
        task_data: TaskCreate
    ) -> Task:
        task = Task(
            user_id=user_id,
            **task_data.model_dump()
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    async def list_tasks(
        self,
        db: Session,
        user_id: int,
        page: int,
        page_size: int,
        **filters
    ) -> TaskListResponse:
        query = select(Task).where(
            Task.user_id == user_id,
            Task.is_deleted == False
        )

        # Apply filters
        if filters.get("status"):
            query = query.where(Task.status == filters["status"])
        if filters.get("priority"):
            query = query.where(Task.priority == filters["priority"])
        if filters.get("search"):
            query = query.where(Task.title.ilike(f"%{filters['search']}%"))

        # Get total count
        total = db.exec(select(func.count()).select_from(query.subquery())).one()

        # Apply pagination
        query = query.offset((page - 1) * page_size).limit(page_size)
        tasks = db.exec(query).all()

        return TaskListResponse(
            items=tasks,
            total=total,
            page=page,
            page_size=page_size,
            pages=(total + page_size - 1) // page_size
        )
```

## Usage Examples

### Generate Task CRUD Endpoints
```
Input: Create endpoints for task management with authentication

Output:
- POST /tasks - Create task
- GET /tasks - List tasks with filters
- GET /tasks/{id} - Get single task
- PATCH /tasks/{id} - Update task
- DELETE /tasks/{id} - Delete task
- POST /tasks/{id}/complete - Mark complete
```

### Generate Chatbot Endpoints
```
Input: Create chatbot message endpoint with session support

Output:
- POST /chat/message - Process user message
- GET /chat/sessions/{id}/history - Get chat history
- DELETE /chat/sessions/{id} - End session
```

## Integration Points

- Uses JWT-Middleware-Generator for authentication
- Works with SQLModel-Schema-Generator for data models
- Integrates with Chatbot-Response-Handler for chat processing
- Coordinates with Task-Coordinator agent for operations
