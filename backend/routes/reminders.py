from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from core.db import get_session
from core.security import get_current_user
from schemas.reminder import ReminderCreate, ReminderResponse, ReminderListResponse
from services.reminder_service import ReminderService
from utils.errors import TaskNotFoundError, UnauthorizedAccessError
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/tasks/{task_id}/reminders", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    task_id: UUID,
    reminder_data: ReminderCreate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ReminderResponse:
    """Create a new reminder for a specific task."""
    try:
        reminder = ReminderService.create_reminder(session, task_id, reminder_data, current_user_id)
        return ReminderResponse.model_validate(reminder, from_attributes=True)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    except UnauthorizedAccessError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to set reminders for this task"
        )
    except Exception as e:
        logger.exception(f"Error creating reminder: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating reminder: {str(e)}"
        )


@router.get("/reminders", response_model=ReminderListResponse)
def get_my_reminders(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ReminderListResponse:
    """Get all reminders for the authenticated user."""
    try:
        reminders = ReminderService.get_reminders_by_user(session, current_user_id)
        reminder_responses = [ReminderResponse.model_validate(r, from_attributes=True) for r in reminders]
        return ReminderListResponse(reminders=reminder_responses, total=len(reminder_responses))
    except Exception as e:
        logger.exception(f"Error fetching reminders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching reminders: {str(e)}"
        )


@router.get("/tasks/{task_id}/reminders", response_model=ReminderListResponse)
def get_task_reminders(
    task_id: UUID,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ReminderListResponse:
    """Get all reminders for a specific task."""
    try:
        reminders = ReminderService.get_reminders_by_task(session, task_id, current_user_id)
        reminder_responses = [ReminderResponse.model_validate(r, from_attributes=True) for r in reminders]
        return ReminderListResponse(reminders=reminder_responses, total=len(reminder_responses))
    except Exception as e:
        logger.exception(f"Error fetching task reminders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching task reminders: {str(e)}"
        )


@router.delete("/reminders/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(
    reminder_id: UUID,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a reminder."""
    try:
        ReminderService.delete_reminder(session, reminder_id, current_user_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reminder with ID {reminder_id} not found"
        )
    except UnauthorizedAccessError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this reminder"
        )
    except Exception as e:
        logger.exception(f"Error deleting reminder: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting reminder: {str(e)}"
        )
