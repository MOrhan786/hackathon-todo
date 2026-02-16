from sqlmodel import Session, select
from sqlalchemy import or_, cast, String
from typing import List, Optional
from uuid import UUID
from models.task import Task, TaskCreate, TaskUpdate, RecurrencePattern
from utils.errors import TaskNotFoundError, UnauthorizedAccessError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class TaskService:
    """
    Service class for handling task-related operations.

    Provides CRUD operations for tasks with user isolation enforcement,
    plus search, sort, tags, recurring tasks, and reminders.
    """

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for the specified user.
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=getattr(task_data, 'priority', 'medium'),
            due_date=getattr(task_data, 'due_date', None),
            tags=getattr(task_data, 'tags', []) or [],
            is_recurring=getattr(task_data, 'is_recurring', False),
            recurrence_pattern=getattr(task_data, 'recurrence_pattern', None),
            recurrence_interval=getattr(task_data, 'recurrence_interval', 1),
            recurrence_end_date=getattr(task_data, 'recurrence_end_date', None),
            reminder_at=getattr(task_data, 'reminder_at', None),
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
        due_after: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        page: int = 1,
        page_size: int = 20
    ) -> List[Task]:
        """
        Get all tasks for the specified user with optional filters, search, and sort.
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

        if due_after:
            statement = statement.where(Task.due_date >= due_after)

        # Search by keyword in title and description
        if search:
            search_term = f"%{search}%"
            statement = statement.where(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term)
                )
            )

        # Filter by tags (check if any of the provided tags are in the task's tags)
        if tags:
            from sqlalchemy import text
            for tag in tags:
                statement = statement.where(
                    cast(Task.tags, String).ilike(f'%"{tag}"%')
                )

        # Sort
        if sort_by:
            sort_column = None
            if sort_by == "due_date":
                sort_column = Task.due_date
            elif sort_by == "priority":
                sort_column = Task.priority
            elif sort_by == "title":
                sort_column = Task.title
            elif sort_by == "created_at":
                sort_column = Task.created_at
            elif sort_by == "updated_at":
                sort_column = Task.updated_at

            if sort_column is not None:
                if sort_order == "desc":
                    statement = statement.order_by(sort_column.desc())
                else:
                    statement = statement.order_by(sort_column.asc())
        else:
            statement = statement.order_by(Task.created_at.desc())

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
        due_before: Optional[datetime] = None,
        due_after: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None
    ) -> int:
        """
        Count tasks for the specified user with optional filters.
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

        if due_after:
            statement = statement.where(Task.due_date >= due_after)

        if search:
            search_term = f"%{search}%"
            statement = statement.where(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term)
                )
            )

        if tags:
            for tag in tags:
                statement = statement.where(
                    cast(Task.tags, String).ilike(f'%"{tag}"%')
                )

        count = session.exec(statement).one()
        return count

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID, user_id: str) -> Task:
        """
        Get a specific task by ID if it belongs to the specified user.
        """
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(str(task_id))

        stored_user_id = str(task.user_id).lower() if task.user_id else ""
        requested_user_id = str(user_id).lower() if user_id else ""

        if stored_user_id != requested_user_id:
            raise UnauthorizedAccessError(str(task_id), user_id)

        return task

    @staticmethod
    def update_task(session: Session, task_id: UUID, task_data: TaskUpdate, user_id: str) -> Task:
        """
        Update a task if it belongs to the specified user.
        """
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(str(task_id))

        stored_user_id = str(task.user_id).lower() if task.user_id else ""
        requested_user_id = str(user_id).lower() if user_id else ""

        if stored_user_id != requested_user_id:
            raise UnauthorizedAccessError(str(task_id), user_id)

        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # If status changed to completed, handle recurring task
        if task_data.status and task_data.status == "completed" and task.is_recurring:
            task.completed_at = datetime.utcnow()
            TaskService._create_next_recurring_task(session, task)

        # If status changed to completed, set completed_at
        if task_data.status and task_data.status == "completed" and not task.completed_at:
            task.completed_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(session: Session, task_id: UUID, user_id: str) -> bool:
        """
        Delete a task if it belongs to the specified user.
        """
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(str(task_id))

        stored_user_id = str(task.user_id).lower() if task.user_id else ""
        requested_user_id = str(user_id).lower() if user_id else ""

        if stored_user_id != requested_user_id:
            raise UnauthorizedAccessError(str(task_id), user_id)

        session.delete(task)
        session.commit()

        return True

    @staticmethod
    def _create_next_recurring_task(session: Session, completed_task: Task) -> Optional[Task]:
        """
        Create the next occurrence of a recurring task when the current one is completed.
        """
        if not completed_task.is_recurring or not completed_task.recurrence_pattern:
            return None

        # Calculate next due date based on recurrence pattern
        base_date = completed_task.due_date or datetime.utcnow()
        interval = completed_task.recurrence_interval or 1

        pattern = completed_task.recurrence_pattern.lower()
        if pattern == RecurrencePattern.DAILY:
            next_due = base_date + timedelta(days=interval)
        elif pattern == RecurrencePattern.WEEKLY:
            next_due = base_date + timedelta(weeks=interval)
        elif pattern == RecurrencePattern.MONTHLY:
            next_due = base_date + relativedelta(months=interval)
        elif pattern == RecurrencePattern.YEARLY:
            next_due = base_date + relativedelta(years=interval)
        else:
            return None

        # Check if recurrence has ended
        if completed_task.recurrence_end_date and next_due > completed_task.recurrence_end_date:
            return None

        # Calculate next reminder if original had one
        next_reminder = None
        if completed_task.reminder_at and completed_task.due_date:
            reminder_offset = completed_task.due_date - completed_task.reminder_at
            next_reminder = next_due - reminder_offset

        # Create the next occurrence
        next_task = Task(
            title=completed_task.title,
            description=completed_task.description,
            priority=completed_task.priority,
            tags=completed_task.tags or [],
            due_date=next_due,
            is_recurring=True,
            recurrence_pattern=completed_task.recurrence_pattern,
            recurrence_interval=completed_task.recurrence_interval,
            recurrence_end_date=completed_task.recurrence_end_date,
            reminder_at=next_reminder,
            parent_task_id=completed_task.parent_task_id or completed_task.id,
            user_id=completed_task.user_id
        )

        session.add(next_task)
        # Don't commit here - let the caller handle the transaction
        return next_task

    @staticmethod
    def get_due_reminders(session: Session, user_id: str) -> List[Task]:
        """
        Get tasks with reminders that are due (reminder_at <= now and not yet sent).
        """
        now = datetime.utcnow()
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.is_deleted == False,
            Task.reminder_at <= now,
            Task.reminder_sent == False,
            Task.status != "completed"
        )
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def mark_reminder_sent(session: Session, task_id: UUID, user_id: str) -> Task:
        """
        Mark a task's reminder as sent.
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        task.reminder_sent = True
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
