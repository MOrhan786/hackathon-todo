# Data Model: Todo In-Memory Python Console App

## Task Entity

### Fields
- **id** (int): Auto-incrementing unique identifier for the task
- **title** (str): Title of the task (required, non-empty)
- **description** (str): Detailed description of the task (required, non-empty)
- **completed** (bool): Completion status of the task (default: False)
- **created_at** (datetime): Timestamp of when the task was created (auto-generated)

### Validation Rules
- `title` must be non-empty string (as per FR-011)
- `description` must be non-empty string (as per FR-011)
- `id` must be unique within the task list
- `completed` defaults to False when creating a new task
- `created_at` is automatically set to current datetime when creating a new task

### State Transitions
- `completed` field can transition from False to True (when marked complete)
- `completed` field can transition from True to False (when marked incomplete)
- All other fields remain constant except through update operations

## Task List Entity

### Fields
- **tasks** (List[Task]): In-memory collection of Task objects
- **next_id** (int): Counter for auto-incrementing task IDs

### Operations
- Add task to list
- Get all tasks from list
- Get task by ID
- Update task by ID
- Delete task by ID
- Toggle completion status by ID

### Constraints
- All operations must complete with response time under 1 second (as per SC-007)
- Input sanitization must be applied to prevent injection attacks (as per FR-012)
- Error messages must be user-friendly when invalid task IDs are provided (as per FR-007)