from fastapi import HTTPException, status
from typing import Optional


class TaskNotFoundError(HTTPException):
    """Raised when a task is not found."""

    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )


class UnauthorizedAccessError(HTTPException):
    """Raised when a user tries to access another user's task."""

    def __init__(self, task_id: str, user_id: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} does not have permission to access task {task_id}"
        )


class ValidationError(HTTPException):
    """Raised when input validation fails."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


def handle_database_error(error: Exception, context: str = "") -> HTTPException:
    """
    Handle database-related errors.

    Args:
        error (Exception): The caught exception
        context (str): Additional context for the error

    Returns:
        HTTPException: Formatted HTTP exception
    """
    error_msg = f"Database error occurred{f' in {context}' if context else ''}: {str(error)}"
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=error_msg
    )