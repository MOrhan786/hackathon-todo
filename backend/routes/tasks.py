from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from core.db import get_session
from core.security import get_current_user
from models.task import Task, TaskCreate, TaskUpdate
from schemas.task import TaskResponse, TaskListResponse, TaskCreate as TaskCreateSchema, TaskUpdate as TaskUpdateSchema, ReminderDueResponse
from services.task_service import TaskService
from services.event_service import emit_task_created, emit_task_updated, emit_task_deleted, emit_task_toggled
from utils.errors import TaskNotFoundError, UnauthorizedAccessError


router = APIRouter()


@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by task status"),
    priority: Optional[str] = Query(None, description="Filter by task priority"),
    due_before: Optional[datetime] = Query(None, description="Filter tasks due before this date"),
    due_after: Optional[datetime] = Query(None, description="Filter tasks due after this date"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by"),
    search: Optional[str] = Query(None, description="Search keyword in title and description"),
    sort_by: Optional[str] = Query(None, description="Sort by: due_date, priority, title, created_at, updated_at"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
) -> TaskListResponse:
    """
    Get all tasks for the authenticated user with optional filters, search, and sort.
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        logger.debug(f"Fetching tasks for user_id: {current_user_id}")

        # Parse comma-separated tags
        tag_list = None
        if tags:
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]

        tasks = TaskService.get_tasks_by_user(
            session,
            current_user_id,
            status_filter=status_filter,
            priority=priority,
            due_before=due_before,
            due_after=due_after,
            tags=tag_list,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size
        )
        logger.debug(f"Retrieved {len(tasks)} tasks")

        task_responses = [TaskResponse.model_validate(task.model_dump()) for task in tasks]
        total = TaskService.count_tasks_by_user(
            session, current_user_id, status_filter, priority,
            due_before, due_after, tag_list, search
        )
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
    background_tasks: BackgroundTasks,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.
    """
    try:
        task = TaskService.create_task(session, task_create, current_user_id)
        task_dict = task.model_dump()
        response = TaskResponse.model_validate(task_dict)
        background_tasks.add_task(emit_task_created, task_dict, current_user_id)
        return response
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.get("/tasks/reminders/due", response_model=ReminderDueResponse)
def get_due_reminders(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ReminderDueResponse:
    """
    Get tasks with reminders that are due and not yet sent.
    Always returns 200 with an empty list if no due reminders or on error.
    """
    try:
        tasks = TaskService.get_due_reminders(session, current_user_id)
        task_responses = [TaskResponse.model_validate(t, from_attributes=True) for t in tasks]
        return ReminderDueResponse(tasks=task_responses, count=len(task_responses))
    except Exception as e:
        import logging
        logging.getLogger(__name__).exception(f"Error checking reminders: {e}")
        return ReminderDueResponse(tasks=[], count=0)


@router.post("/tasks/{task_id}/reminder-sent", response_model=TaskResponse)
def mark_reminder_sent(
    task_id: UUID,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Mark a task's reminder as sent (called after notification is delivered).
    """
    try:
        task = TaskService.mark_reminder_sent(session, task_id, current_user_id)
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


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a specific task by ID if it belongs to the authenticated user.
    """
    try:
        task = TaskService.get_task_by_id(session, task_id, current_user_id)
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
    background_tasks: BackgroundTasks,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update a task if it belongs to the authenticated user.
    Completing a recurring task will auto-create the next occurrence.
    """
    try:
        task = TaskService.update_task(session, task_id, task_update, current_user_id)
        task_dict = task.model_dump()
        response = TaskResponse.model_validate(task_dict)
        background_tasks.add_task(emit_task_updated, task_dict, current_user_id)
        return response
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


@router.patch("/tasks/{task_id}/toggle", response_model=TaskResponse)
def toggle_task_completion(
    task_id: UUID,
    background_tasks: BackgroundTasks,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Toggle a task's completion status.
    """
    try:
        task = TaskService.get_task_by_id(session, task_id, current_user_id)
        new_status = "pending" if task.status == "completed" else "completed"
        update_data = TaskUpdate(status=new_status)
        updated_task = TaskService.update_task(session, task_id, update_data, current_user_id)
        task_dict = updated_task.model_dump()
        response = TaskResponse.model_validate(task_dict)
        background_tasks.add_task(emit_task_toggled, task_dict, current_user_id)
        return response
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
            detail=f"Error toggling task: {str(e)}"
        )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    background_tasks: BackgroundTasks,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task if it belongs to the authenticated user.
    """
    try:
        TaskService.delete_task(session, task_id, current_user_id)
        background_tasks.add_task(emit_task_deleted, str(task_id), current_user_id)
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
