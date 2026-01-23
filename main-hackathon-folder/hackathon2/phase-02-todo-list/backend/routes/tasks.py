from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from core.db import get_session
from core.security import get_current_user
from models.task import Task as TaskModel, TaskCreate, TaskUpdate
from schemas.task import TaskResponse, TaskListResponse, TaskCreate as TaskCreateSchema, TaskUpdate as TaskUpdateSchema
from services.task_service import TaskService
from utils.errors import TaskNotFoundError, UnauthorizedAccessError


router = APIRouter()


@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskListResponse:
    """
    Get all tasks for the authenticated user.

    Args:
        current_user_id: ID of the authenticated user (extracted from JWT)
        session: Database session

    Returns:
        TaskListResponse: List of tasks belonging to the user
    """
    try:
        tasks = TaskService.get_tasks_by_user(session, current_user_id)
        return TaskListResponse(tasks=tasks)
    except Exception as e:
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
        current_user_id: ID of the authenticated user (extracted from JWT)
        session: Database session

    Returns:
        TaskResponse: Created task
    """
    try:
        task = TaskService.create_task(session, task_create, current_user_id)
        return task
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
        current_user_id: ID of the authenticated user (extracted from JWT)
        session: Database session

    Returns:
        TaskResponse: The requested task
    """
    try:
        task = TaskService.get_task_by_id(session, task_id, current_user_id)
        return task
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
        current_user_id: ID of the authenticated user (extracted from JWT)
        session: Database session

    Returns:
        TaskResponse: Updated task
    """
    try:
        # Convert schema to model and update
        task = TaskService.get_task_by_id(session, task_id, current_user_id)

        # Update the task with provided data
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        session.add(task)
        session.commit()
        session.refresh(task)

        return task
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
        current_user_id: ID of the authenticated user (extracted from JWT)
        session: Database session
    """
    try:
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