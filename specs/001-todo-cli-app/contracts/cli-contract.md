# API Contract: Todo In-Memory Python Console App

## CLI Commands Interface

### Add Task Command
- **Command**: `add`
- **Arguments**:
  - `--title` (required, str): Title of the task
  - `--description` (required, str): Description of the task
- **Output**: "Task added successfully with ID: {id}"
- **Error Cases**: 
  - If title or description is empty: "Error: Title and description cannot be empty"

### List Tasks Command
- **Command**: `list`
- **Arguments**: None
- **Output**: Tabular display of all tasks with ID, Status ([ ]/[x]), Title, truncated Description, and Created date
- **Empty Case**: "No tasks added yet."

### Update Task Command
- **Command**: `update`
- **Arguments**:
  - `--id` (required, int): ID of the task to update
  - `--title` (optional, str): New title for the task
  - `--description` (optional, str): New description for the task
- **Output**: "Task {id} updated successfully"
- **Error Cases**: 
  - If task ID not found: "Error: Task with ID {id} not found"
  - If no fields to update: "Error: Please provide at least one field to update (title or description)"

### Delete Task Command
- **Command**: `delete`
- **Arguments**:
  - `--id` (required, int): ID of the task to delete
- **Output**: "Task {id} deleted successfully"
- **Error Cases**: 
  - If task ID not found: "Error: Task with ID {id} not found"

### Complete Task Command
- **Command**: `complete`
- **Arguments**:
  - `--id` (required, int): ID of the task to toggle
- **Output**: "Task {id} completed" or "Task {id} marked as incomplete"
- **Error Cases**: 
  - If task ID not found: "Error: Task with ID {id} not found"

## Data Models

### Task
```python
{
  "id": int,
  "title": str,
  "description": str,
  "completed": bool,
  "created_at": datetime
}
```

## Error Response Format
```python
{
  "error": "Error message describing the issue"
}
```

## Performance Requirements
- All operations must complete with response time under 1 second
- Input sanitization must be applied to prevent injection attacks