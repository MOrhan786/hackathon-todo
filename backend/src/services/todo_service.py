from typing import List, Optional
from sqlmodel import Session, select
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User
from uuid import UUID
from datetime import datetime


class TodoService:
    """Service class for todo-related operations."""

    @staticmethod
    def get_todo_by_id(session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """
        Retrieve a specific todo by ID for a specific user.

        Args:
            session: Database session
            todo_id: Todo's UUID
            user_id: User's UUID (to ensure user isolation)

        Returns:
            Todo object if found and owned by user, None otherwise
        """
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_todos_for_user(
        session: Session,
        user_id: UUID,
        completed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Todo]:
        """
        Retrieve all todos for a specific user with optional filtering.

        Args:
            session: Database session
            user_id: User's UUID
            completed: Filter by completion status (optional)
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            List of Todo objects belonging to the user
        """
        statement = select(Todo).where(Todo.user_id == user_id)

        if completed is not None:
            statement = statement.where(Todo.completed == completed)

        statement = statement.offset(offset).limit(limit)
        results = session.exec(statement).all()
        return results

    @staticmethod
    def create_todo(session: Session, todo_create: TodoCreate, user_id: UUID) -> Todo:
        """
        Create a new todo for a specific user.

        Args:
            session: Database session
            todo_create: Todo creation data
            user_id: User's UUID

        Returns:
            Created Todo object
        """
        db_todo = Todo(
            title=todo_create.title,
            description=todo_create.description,
            completed=todo_create.completed,
            user_id=user_id
        )

        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)

        return db_todo

    @staticmethod
    def update_todo(session: Session, todo_id: UUID, todo_update: TodoUpdate, user_id: UUID) -> Optional[Todo]:
        """
        Update a todo for a specific user.

        Args:
            session: Database session
            todo_id: Todo's UUID
            todo_update: Todo update data
            user_id: User's UUID (to ensure user isolation)

        Returns:
            Updated Todo object if successful, None if todo not found or not owned by user
        """
        db_todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not db_todo:
            return None

        # Update fields that are provided
        update_data = todo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)

        db_todo.updated_at = datetime.utcnow()
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)

        return db_todo

    @staticmethod
    def delete_todo(session: Session, todo_id: UUID, user_id: UUID) -> bool:
        """
        Delete a todo for a specific user.

        Args:
            session: Database session
            todo_id: Todo's UUID
            user_id: User's UUID (to ensure user isolation)

        Returns:
            True if deletion was successful, False if todo not found or not owned by user
        """
        db_todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not db_todo:
            return False

        session.delete(db_todo)
        session.commit()
        return True