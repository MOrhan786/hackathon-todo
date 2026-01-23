from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID
from ..database import get_session
from ..middleware.auth import get_current_user
from ..models.user import User
from ..models.todo import TodoCreate, TodoUpdate, TodoResponse
from ..services.todo_service import TodoService
from ..services.user_service import UserService

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=List[TodoResponse])
def get_todos(
    current_user: User = Depends(get_current_user),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    session: Session = Depends(get_session)
):
    """
    Get authenticated user's todos with optional filtering.

    Args:
        current_user: The authenticated user
        completed: Filter by completion status (optional)
        limit: Maximum number of results to return
        offset: Number of results to skip
        session: Database session

    Returns:
        List[TodoResponse]: List of user's todos
    """
    todos = TodoService.get_todos_for_user(
        session=session,
        user_id=current_user.id,
        completed=completed,
        limit=limit,
        offset=offset
    )

    return todos


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the authenticated user.

    Args:
        todo_create: Todo creation data
        current_user: The authenticated user
        session: Database session

    Returns:
        TodoResponse: The created todo
    """
    todo = TodoService.create_todo(
        session=session,
        todo_create=todo_create,
        user_id=current_user.id
    )

    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a todo for the authenticated user.

    Args:
        todo_id: ID of the todo to update
        todo_update: Todo update data
        current_user: The authenticated user
        session: Database session

    Returns:
        TodoResponse: The updated todo

    Raises:
        HTTPException: If todo doesn't exist or doesn't belong to user
    """
    todo = TodoService.update_todo(
        session=session,
        todo_id=todo_id,
        todo_update=todo_update,
        user_id=current_user.id
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to user"
        )

    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a todo for the authenticated user.

    Args:
        todo_id: ID of the todo to delete
        current_user: The authenticated user
        session: Database session

    Raises:
        HTTPException: If todo doesn't exist or doesn't belong to user
    """
    success = TodoService.delete_todo(
        session=session,
        todo_id=todo_id,
        user_id=current_user.id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to user"
        )


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo for the authenticated user.

    Args:
        todo_id: ID of the todo to retrieve
        current_user: The authenticated user
        session: Database session

    Returns:
        TodoResponse: The requested todo

    Raises:
        HTTPException: If todo doesn't exist or doesn't belong to user
    """
    todo = TodoService.get_todo_by_id(
        session=session,
        todo_id=todo_id,
        user_id=current_user.id
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or does not belong to user"
        )

    return todo