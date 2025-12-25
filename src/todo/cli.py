"""
Command-line interface for the Todo In-Memory Python Console App.
"""
import argparse
import sys
from typing import List
from datetime import datetime
from .models import Task
from .storage import InMemoryTaskStorage


class TodoCLI:
    """
    Command-line interface for the Todo application using argparse.
    """
    def __init__(self):
        self.storage = InMemoryTaskStorage()

    def add_task(self, title: str, description: str) -> None:
        """
        Add a new task to the list.

        Args:
            title: The title of the task
            description: The description of the task
        """
        task = self.storage.add_task(title, description)
        print(f"Task added successfully with ID: {task.id}")
        print("Next: Try 'list' to view all tasks")

    def list_tasks(self) -> None:
        """
        List all tasks in a tabular format with status indicators.
        """
        tasks = self.storage.get_all_tasks()

        if not tasks:
            print("No tasks added yet.")
            print("Next: Try 'add --title \"Task\" --description \"Details\"' to add your first task")
            return

        # Print table header
        print(f"{'ID':<4} {'Status':<7} {'Title':<20} {'Description':<30} {'Created':<12}")
        print("-" * 80)

        # Print each task
        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            truncated_desc = task.description[:25] + "..." if len(task.description) > 25 else task.description
            created_date = task.created_at.strftime("%Y-%m-%d")
            print(f"{task.id:<4} {status:<7} {task.title[:19]:<20} {truncated_desc:<30} {created_date:<12}")

        if tasks:
            print("Next: Try 'complete <id>' or 'update <id>' to manage tasks")

    def update_task(self, task_id: int, title: str = None, description: str = None) -> None:
        """
        Update task details by ID.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
        """
        # Only update if at least one field is provided
        if title is None and description is None:
            print("Error: Please provide at least one field to update (title or description)")
            return

        success = self.storage.update_task(task_id, title, description)
        if success:
            print(f"Task {task_id} updated successfully")
        else:
            print(f"Error: Task with ID {task_id} not found")
            return

        print("Next: Try 'list' to see changes")

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete
        """
        success = self.storage.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Error: Task with ID {task_id} not found")
            return

        print("Next: Try 'list' to see changes")

    def complete_task(self, task_id: int) -> None:
        """
        Toggle the completion status of a task by ID.

        Args:
            task_id: The ID of the task to toggle
        """
        success = self.storage.toggle_task_status(task_id)
        if success:
            task = self.storage.get_task_by_id(task_id)
            status = "completed" if task.completed else "marked as incomplete"
            print(f"Task {task_id} {status}")
        else:
            print(f"Error: Task with ID {task_id} not found")
            return

        print("Next: Try 'list' to see updated status")

    def show_interactive_menu(self) -> None:
        """
        Show an interactive menu when no arguments are provided.
        """
        print("""
+============================================================================+
|                           Welcome to Todo CLI App!                         |
|                                                                              |
|  Manage your tasks efficiently from the command line.                      |
|  All data is stored in-memory and resets when you exit.                    |
+============================================================================+
        """)

        while True:
            print("\nPlease select an option:")
            print("1. Add a new task")
            print("2. List all tasks")
            print("3. Update a task")
            print("4. Delete a task")
            print("5. Mark task as complete/incomplete")
            print("6. Exit")

            try:
                choice = input("\nEnter your choice (1-6): ").strip()

                if choice == '1':
                    title = input("Enter task title: ").strip()
                    description = input("Enter task description: ").strip()
                    if title and description:
                        self.add_task(title, description)
                    else:
                        print("Error: Both title and description are required.")

                elif choice == '2':
                    self.list_tasks()

                elif choice == '3':
                    try:
                        task_id = int(input("Enter task ID to update: ").strip())
                        title = input("Enter new title (or press Enter to skip): ").strip()
                        description = input("Enter new description (or press Enter to skip): ").strip()

                        # Only update if at least one field is provided
                        if title or description:
                            title = title if title else None
                            description = description if description else None
                            self.update_task(task_id, title, description)
                        else:
                            print("Error: Please provide at least one field to update (title or description)")
                    except ValueError:
                        print("Error: Please enter a valid task ID (number).")

                elif choice == '4':
                    try:
                        task_id = int(input("Enter task ID to delete: ").strip())
                        self.delete_task(task_id)
                    except ValueError:
                        print("Error: Please enter a valid task ID (number).")

                elif choice == '5':
                    try:
                        task_id = int(input("Enter task ID to toggle: ").strip())
                        self.complete_task(task_id)
                    except ValueError:
                        print("Error: Please enter a valid task ID (number).")

                elif choice == '6':
                    print("Goodbye!")
                    break

                else:
                    print("Invalid choice. Please enter a number between 1-6.")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break

    def _create_parser(self):
        """
        Create and return the argument parser.
        """
        parser = argparse.ArgumentParser(
            description="Todo In-Memory Python Console App",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s add --title "Buy groceries" --description "Milk, bread, eggs"
  %(prog)s list
  %(prog)s update 1 --title "Updated title"
  %(prog)s delete 1
  %(prog)s complete 1
            """
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Add command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('--title', required=True, help='Title of the task')
        add_parser.add_argument('--description', required=True, help='Description of the task')

        # List command
        list_parser = subparsers.add_parser('list', help='List all tasks')

        # Update command
        update_parser = subparsers.add_parser('update', help='Update a task')
        update_parser.add_argument('id', type=int, help='ID of the task to update')
        update_parser.add_argument('--title', help='New title of the task')
        update_parser.add_argument('--description', help='New description of the task')

        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('id', type=int, help='ID of the task to delete')

        # Complete command
        complete_parser = subparsers.add_parser('complete', help='Toggle task completion status')
        complete_parser.add_argument('id', type=int, help='ID of the task to toggle')

        return parser

    def run(self) -> None:
        """
        Run the command-line interface.
        """
        # Check if no arguments were provided
        if len(sys.argv) == 1:
            self.show_interactive_menu()
            return

        parser = self._create_parser()
        args = parser.parse_args()

        # Execute the appropriate command
        if args.command == 'add':
            self.add_task(args.title, args.description)
        elif args.command == 'list':
            self.list_tasks()
        elif args.command == 'update':
            self.update_task(args.id, args.title, args.description)
        elif args.command == 'delete':
            self.delete_task(args.id)
        elif args.command == 'complete':
            self.complete_task(args.id)
        else:
            parser.print_help()