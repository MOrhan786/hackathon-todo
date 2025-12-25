"""
In-memory storage operations for the Todo In-Memory Python Console App.
"""
from typing import List, Optional
from .models import Task


class InMemoryTaskStorage:
    """
    Manages in-memory storage of tasks using a list.
    """
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: str) -> Task:
        """
        Add a new task to the storage.
        
        Args:
            title: The title of the task
            description: The description of the task
            
        Returns:
            The newly created Task object
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks from storage.
        
        Returns:
            List of all Task objects
        """
        return self._tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update a task's title or description by ID.
        
        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
            
        Returns:
            True if the task was updated, False otherwise
        """
        task = self.get_task_by_id(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was deleted, False otherwise
        """
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def toggle_task_status(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task by ID.
        
        Args:
            task_id: The ID of the task to toggle
            
        Returns:
            True if the task status was toggled, False otherwise
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = not task.completed
            return True
        return False