# Quickstart Guide: Todo In-Memory Python Console App

## Prerequisites

- Python 3.13+
- UV package manager

## Installation

1. Clone the repository
2. Navigate to the project directory

## Usage

### Adding a Task
```bash
uv run src/todo/__main__.py add --title "Task Title" --description "Task Description"
```

### Listing All Tasks
```bash
uv run src/todo/__main__.py list
```

### Updating a Task
```bash
uv run src/todo/__main__.py update --id 1 --title "New Title" --description "New Description"
```

### Deleting a Task
```bash
uv run src/todo/__main__.py delete --id 1
```

### Marking a Task as Complete/Incomplete
```bash
uv run src/todo/__main__.py complete --id 1
```

### Using the Simplified Commands
If you've set up the simplified commands (todo.bat/todo.sh), you can use:
```bash
todo add --title "Task Title" --description "Task Description"
todo list
todo update --id 1 --title "New Title"
todo delete --id 1
todo complete --id 1
```

## Expected Output Format

The `list` command displays tasks in a tabular format:
```
ID   Status  Title               Description          Created
--------------------------------------------------------------------------------
1    [ ]     Sample Task Title   Sample Description   2025-12-25
2    [x]     Completed Task      Task description     2025-12-25
```

For an empty list, it shows: "No tasks added yet."

## Error Handling

When an invalid task ID is provided, the application shows a clear error message:
```
Error: Task with ID X not found
```

## Validation

The application validates that required fields (title and description) are non-empty when adding or updating tasks.