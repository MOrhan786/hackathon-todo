"""
__init__.py for the Todo In-Memory Python Console App package.
"""
from .models import Task
from .storage import InMemoryTaskStorage
from .cli import TodoCLI

__version__ = "1.0.0"
__author__ = "Todo App Development Team"
__description__ = "A command-line Todo application that stores tasks only in memory"