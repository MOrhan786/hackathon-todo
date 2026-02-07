from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from models.task import Task, TaskCreate, TaskUpdate
from utils.errors import TaskNotFoundError, UnauthorizedAccessError
from datetime import datetime


class TaskService:
    """
    Service class for handling task-related operations.

    Provides CRUD operations for tasks with user isolation enforcement.
    """

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for the specified user.

        Args:
            session: Database session
            task_data: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Created Task object
        """
        # Create task with user_id injected and let SQLModel handle default values for timestamps
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            user_id=user_id
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: str,
        status_filter: Optional[str] = None,
        priority: Optional[str] = None,
        due_before: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[Task]:
        """
        Get all tasks for the specified user with optional filters.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            status_filter: Filter by task status
            priority: Filter by priority
            due_before: Filter tasks due before this date
            page: Page number for pagination
            page_size: Number of items per page

        Returns:
            List of Task objects belonging to the user
        """
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.is_deleted == False
        )

        if status_filter:
            statement = statement.where(Task.status == status_filter)

        if priority:
            statement = statement.where(Task.priority == priority)

        if due_before:
            statement = statement.where(Task.due_date <= due_before)

        # Pagination
        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)

        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def count_tasks_by_user(
        session: Session,
        user_id: str,
        status_filter: Optional[str] = None,
        priority: Optional[str] = None,
        due_before: Optional[datetime] = None
    ) -> int:
        """
        Count tasks for the specified user with optional filters.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to count
            status_filter: Filter by task status
            priority: Filter by priority
            due_before: Filter tasks due before this date

        Returns:
            Count of tasks matching the filters
        """
        from sqlalchemy import func as sql_func

        statement = select(sql_func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.is_deleted == False
        )

        if status_filter:
            statement = statement.where(Task.status == status_filter)

        if priority:
            statement = statement.where(Task.priority == priority)

        if due_before:
            statement = statement.where(Task.due_date <= due_before)

        count = session.exec(statement).one()
        return count

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID, user_id: str) -> Task:
        """
        Get a specific task by ID if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user requesting the task

        Returns:
            Task object if it belongs to the user

        Raises:
            TaskNotFoundError: If task doesn't exist
            UnauthorizedAccessError: If task doesn't belong to user
        """
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(str(task_id))

        # Normalize both user IDs to lowercase to handle potential case differences in UUID string representation
        stored_user_id = str(task.user_id).lower() if task.user_id else ""
        requested_user_id = str(user_id).lower() if user_id else ""

        if stored_user_id != requested_user_id:
            raise UnauthorizedAccessError(str(task_id), user_id)

        return task

    @staticmethod
    def update_task(session: Session, task_id: UUID, task_data: TaskUpdate, user_id: str) -> Task:
        """
        Update a task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            task_data: Task update data
            user_id: ID of the user requesting the update

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task doesn't exist
            UnauthorizedAccessError: If task doesn't belong to user
        """
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(str(task_id))

        # Normalize both user IDs to lowercase to handle potential case differences in UUID string representation
        stored_user_id = str(task.user_id).lower() if task.user_id else ""
        requested_user_id = str(user_id).lower() if user_id else ""

        if stored_user_id != requested_user_id:
            raise UnauthorizedAccessError(str(task_id), user_id)

        # Update the task with provided data
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(session: Session, task_id: UUID, user_id: str) -> bool:
        """
        Delete a task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user requesting the deletion

        Returns:
            True if task was deleted

        Raises:
            TaskNotFoundError: If task doesn't exist
            UnauthorizedAccessError: If task doesn't belong to user
        """
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(str(task_id))

        # Normalize both user IDs to lowercase to handle potential case differences in UUID string representation
        stored_user_id = str(task.user_id).lower() if task.user_id else ""
        requested_user_id = str(user_id).lower() if user_id else ""

        if stored_user_id != requested_user_id:
            raise UnauthorizedAccessError(str(task_id), user_id)

        session.delete(task)
        session.commit()

        return True