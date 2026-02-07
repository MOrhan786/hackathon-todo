"""
Task management tools for OpenAI agent function calling.

These tools wrap TaskService methods and provide them as callable functions
for the AI agent with proper schemas.
"""

from typing import Dict, List, Optional, Any
from uuid import UUID
from sqlmodel import Session
from services.task_service import TaskService
from models.task import TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from datetime import datetime
import json


# Tool schemas for OpenAI function calling
TASK_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user with optional priority and due date",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The task title (required, 1-255 characters)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the task (optional)"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "Task priority level (default: medium)"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in ISO format (YYYY-MM-DD) or natural language like 'tomorrow', 'next week'"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List user's tasks with optional filters for status and priority",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed"],
                        "description": "Filter tasks by status"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "Filter tasks by priority"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to complete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update task fields like title, description, priority, or status",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "New priority level"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed"],
                        "description": "New task status"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in ISO format (YYYY-MM-DD)"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Permanently delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]


class TaskToolExecutor:
    """
    Executor class for task management tools.

    Handles execution of tool calls from the AI agent.
    """

    def __init__(self, session: Session, user_id: str):
        """
        Initialize the tool executor.

        Args:
            session: Database session for operations
            user_id: ID of the user making requests
        """
        self.session = session
        self.user_id = user_id

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by name with the provided arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Dictionary of arguments for the tool

        Returns:
            Result dictionary with success status and data
        """
        try:
            if tool_name == "add_task":
                return self._add_task(**arguments)
            elif tool_name == "list_tasks":
                return self._list_tasks(**arguments)
            elif tool_name == "complete_task":
                return self._complete_task(**arguments)
            elif tool_name == "update_task":
                return self._update_task(**arguments)
            elif tool_name == "delete_task":
                return self._delete_task(**arguments)
            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new task."""
        try:
            # Parse due_date if provided
            parsed_due_date = None
            if due_date:
                try:
                    parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    # If parsing fails, leave it as None
                    pass

            task_data = TaskCreate(
                title=title,
                description=description,
                priority=TaskPriority(priority),
                due_date=parsed_due_date
            )

            task = TaskService.create_task(self.session, task_data, self.user_id)

            return {
                "success": True,
                "task_id": str(task.id),
                "title": task.title,
                "status": task.status.value,
                "priority": task.priority.value,
                "message": f"Task '{task.title}' created successfully"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to create task: {str(e)}"}

    def _list_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> Dict[str, Any]:
        """List user's tasks with optional filters."""
        try:
            tasks = TaskService.get_tasks_by_user(
                self.session,
                self.user_id,
                status_filter=status,
                priority=priority
            )

            task_list = [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "description": t.description,
                    "status": t.status.value,
                    "priority": t.priority.value,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                    "created_at": t.created_at.isoformat()
                }
                for t in tasks
            ]

            return {
                "success": True,
                "count": len(task_list),
                "tasks": task_list,
                "message": f"Found {len(task_list)} task(s)"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to list tasks: {str(e)}"}

    def _complete_task(self, task_id: str) -> Dict[str, Any]:
        """Mark a task as completed."""
        try:
            task = TaskService.update_task(
                self.session,
                UUID(task_id),
                TaskUpdate(status=TaskStatus.COMPLETED),
                self.user_id
            )

            return {
                "success": True,
                "task_id": str(task.id),
                "title": task.title,
                "message": f"Task '{task.title}' marked as completed"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to complete task: {str(e)}"}

    def _update_task(self, task_id: str, **updates) -> Dict[str, Any]:
        """Update task fields."""
        try:
            # Parse due_date if provided
            if 'due_date' in updates and updates['due_date']:
                try:
                    updates['due_date'] = datetime.fromisoformat(updates['due_date'].replace('Z', '+00:00'))
                except ValueError:
                    del updates['due_date']

            # Convert string enums to proper types
            if 'priority' in updates:
                updates['priority'] = TaskPriority(updates['priority'])
            if 'status' in updates:
                updates['status'] = TaskStatus(updates['status'])

            task = TaskService.update_task(
                self.session,
                UUID(task_id),
                TaskUpdate(**updates),
                self.user_id
            )

            return {
                "success": True,
                "task_id": str(task.id),
                "title": task.title,
                "message": f"Task '{task.title}' updated successfully"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to update task: {str(e)}"}

    def _delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task permanently."""
        try:
            success = TaskService.delete_task(
                self.session,
                UUID(task_id),
                self.user_id
            )

            return {
                "success": success,
                "task_id": task_id,
                "message": "Task deleted successfully"
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to delete task: {str(e)}"}
