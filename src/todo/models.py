"""
Task dataclass for the Todo In-Memory Python Console App.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    """
    Represents a single todo task with id, title, description, completion status, and creation timestamp.
    """
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        """
        Initialize the created_at field if not provided.
        """
        if self.created_at is None:
            self.created_at = datetime.now()

    def __str__(self) -> str:
        """
        String representation of the task for display purposes.
        """
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.id}: {self.title} - {self.description[:50]}{'...' if len(self.description) > 50 else ''}"