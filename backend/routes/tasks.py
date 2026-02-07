from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from core.db import get_session
from core.security import get_current_user
from models.task import Task, TaskCreate, TaskUpdate
from schemas.task import TaskResponse, TaskListResponse, TaskCreate as TaskCreateSchema, TaskUpdate as TaskUpdateSchema
from services.task_service import TaskService
from utils.errors import TaskNotFoundError, UnauthorizedAccessError


router = APIRouter()


@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by task status"),
    priority: Optional[str] = Query(None, description="Filter by task priority"),
    due_before: Optional[datetime] = Query(None, description="Filter tasks due before this date"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
) -> TaskListResponse:
    """
    Get all tasks for the authenticated user with optional filters.

    Args:
        current_user_id: The authenticated user ID (extracted from JWT)
        session: Database session
        status_filter: Filter by task status (pending/in_progress/completed)
        priority: Filter by priority (low/medium/high/urgent)
        due_before: Filter tasks due before this date
        page: Page number for pagination
        page_size: Number of items per page

    Returns:
        TaskListResponse: Filtered list of tasks belonging to the user
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        # current_user_id is already a string from JWT
        logger.debug(f"Fetching tasks for user_id: {current_user_id}")

        tasks = TaskService.get_tasks_by_user(
            session,
            current_user_id,
            status_filter=status_filter,
            priority=priority,
            due_before=due_before,
            page=page,
            page_size=page_size
        )
        logger.debug(f"Retrieved {len(tasks)} tasks")

        # Convert SQLModel objects to Pydantic response objects by converting to dict first
        task_responses = [TaskResponse.model_validate(task.model_dump()) for task in tasks]
        total = TaskService.count_tasks_by_user(session, current_user_id, status_filter, priority, due_before)
        return TaskListResponse(
            tasks=task_responses,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.exception(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreateSchema,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Args:
        task_create: Task creation data
        current_user_id: The authenticated user ID (extracted from JWT)
        session: Database session

    Returns:
        TaskResponse: Created task
    """
    try:
        # current_user_id is already a string from JWT
        task = TaskService.create_task(session, task_create, current_user_id)
        # Convert SQLModel object to Pydantic response object by converting to dict first
        return TaskResponse.model_validate(task.model_dump())
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a specific task by ID if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to retrieve
        current_user_id: The authenticated user ID (extracted from JWT)
        session: Database session

    Returns:
        TaskResponse: The requested task
    """
    try:
        # current_user_id is already a string from JWT
        task = TaskService.get_task_by_id(session, task_id, current_user_id)
        # Convert SQLModel object to Pydantic response object by converting to dict first
        return TaskResponse.model_validate(task.model_dump())
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    except UnauthorizedAccessError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to access this task"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving task: {str(e)}"
        )


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_update: TaskUpdateSchema,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update a task if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to update
        task_update: Task update data
        current_user_id: The authenticated user ID (extracted from JWT)
        session: Database session

    Returns:
        TaskResponse: Updated task
    """
    try:
        # current_user_id is already a string from JWT

        # Get the task to ensure it belongs to the user
        task = TaskService.get_task_by_id(session, task_id, current_user_id)

        # Update the task with provided data
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        session.add(task)
        session.commit()
        session.refresh(task)

        # Convert SQLModel object to Pydantic response object by converting to dict first
        return TaskResponse.model_validate(task.model_dump())
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    except UnauthorizedAccessError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to update this task"
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to delete
        current_user_id: The authenticated user ID (extracted from JWT)
        session: Database session
    """
    try:
        # current_user_id is already a string from JWT
        TaskService.delete_task(session, task_id, current_user_id)
        return
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    except UnauthorizedAccessError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to delete this task"
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )