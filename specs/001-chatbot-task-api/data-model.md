# Data Model: AI-Powered Todo Chatbot Backend API

**Feature**: 001-chatbot-task-api
**Date**: 2025-02-05

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────────┐
│    User     │       │    Task     │       │  TaskReminder   │
├─────────────┤       ├─────────────┤       ├─────────────────┤
│ id (PK)     │──1:N──│ user_id (FK)│       │ id (PK)         │
│ email       │       │ id (PK)     │──1:N──│ task_id (FK)    │
│ password_   │       │ title       │       │ user_id (FK)    │
│   hash      │       │ description │       │ remind_at       │
│ created_at  │       │ status      │       │ is_sent         │
│ updated_at  │       │ priority    │       │ sent_at         │
└─────────────┘       │ due_date    │       │ created_at      │
                      │ completed_at│       └─────────────────┘
                      │ is_deleted  │
                      │ created_at  │
                      │ updated_at  │
                      └─────────────┘
```

## Entity Definitions

### User (Existing)

Represents an authenticated user of the system.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | Account creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT now() | Last update time |

**Indexes**:
- `idx_user_email` on `email` (unique)

### Task (Modified)

Represents a todo item owned by a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| user_id | VARCHAR(255) | NOT NULL, INDEX | Owner's user ID |
| title | VARCHAR(255) | NOT NULL | Task title (1-255 chars) |
| description | TEXT | NULL, DEFAULT '' | Optional description |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending/in_progress/completed |
| priority | VARCHAR(10) | NOT NULL, DEFAULT 'medium' | low/medium/high/urgent |
| due_date | TIMESTAMP | NULL | Optional due date |
| completed_at | TIMESTAMP | NULL | When task was completed |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT false | Soft delete flag |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT now() | Last update timestamp |

**Indexes**:
- `idx_task_user_id` on `user_id`
- `idx_task_user_status` on `(user_id, status)` - for filtered queries
- `idx_task_user_due` on `(user_id, due_date)` - for due date queries
- `idx_task_user_deleted` on `(user_id, is_deleted)` - for active task queries

**Constraints**:
- `chk_task_status` CHECK (status IN ('pending', 'in_progress', 'completed'))
- `chk_task_priority` CHECK (priority IN ('low', 'medium', 'high', 'urgent'))

### TaskReminder (New)

Represents a scheduled reminder for a task.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| task_id | UUID | NOT NULL, FK(tasks.id) | Associated task |
| user_id | VARCHAR(255) | NOT NULL, INDEX | Owner's user ID (denormalized) |
| remind_at | TIMESTAMP | NOT NULL, INDEX | When to send reminder |
| is_sent | BOOLEAN | NOT NULL, DEFAULT false | Whether reminder was sent |
| sent_at | TIMESTAMP | NULL | When reminder was sent |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | Creation timestamp |

**Indexes**:
- `idx_reminder_task` on `task_id`
- `idx_reminder_user` on `user_id`
- `idx_reminder_pending` on `(is_sent, remind_at)` - for reminder processing
- `idx_reminder_user_task` on `(user_id, task_id)` - for user-specific queries

**Foreign Keys**:
- `fk_reminder_task` FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE

## SQLModel Definitions

### Task Model (Updated)

```python
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func, Enum
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
import enum


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(SQLModel):
    """Base class for Task model."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default="", max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """Task model for database."""
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)
    completed_at: Optional[datetime] = Field(default=None)
    is_deleted: bool = Field(default=False, index=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass


class TaskUpdate(SQLModel):
    """Model for updating an existing task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    """Model for reading task data."""
    id: UUID
    user_id: str
    completed_at: Optional[datetime]
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
```

### TaskReminder Model (New)

```python
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class TaskReminderBase(SQLModel):
    """Base class for TaskReminder model."""
    remind_at: datetime


class TaskReminder(TaskReminderBase, table=True):
    """TaskReminder model for database."""
    __tablename__ = "task_reminders"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_id: UUID = Field(foreign_key="tasks.id", index=True)
    user_id: str = Field(index=True)
    is_sent: bool = Field(default=False)
    sent_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )


class ReminderCreate(TaskReminderBase):
    """Model for creating a reminder."""
    pass


class ReminderRead(TaskReminderBase):
    """Model for reading reminder data."""
    id: UUID
    task_id: UUID
    user_id: str
    is_sent: bool
    sent_at: Optional[datetime]
    created_at: datetime
```

## Migration Strategy

### Migration 001: Add Task Fields

```sql
-- Add new columns to tasks table
ALTER TABLE tasks
    ADD COLUMN priority VARCHAR(10) NOT NULL DEFAULT 'medium',
    ADD COLUMN due_date TIMESTAMP NULL,
    ADD COLUMN completed_at TIMESTAMP NULL,
    ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT false;

-- Update status constraint to include 'in_progress'
-- Note: May need to drop and recreate constraint
ALTER TABLE tasks
    DROP CONSTRAINT IF EXISTS chk_task_status;
ALTER TABLE tasks
    ADD CONSTRAINT chk_task_status
    CHECK (status IN ('pending', 'in_progress', 'completed'));

-- Add priority constraint
ALTER TABLE tasks
    ADD CONSTRAINT chk_task_priority
    CHECK (priority IN ('low', 'medium', 'high', 'urgent'));

-- Add indexes
CREATE INDEX idx_task_user_status ON tasks(user_id, status);
CREATE INDEX idx_task_user_due ON tasks(user_id, due_date);
CREATE INDEX idx_task_user_deleted ON tasks(user_id, is_deleted);
```

### Migration 002: Create TaskReminders Table

```sql
-- Create task_reminders table
CREATE TABLE task_reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL,
    remind_at TIMESTAMP NOT NULL,
    is_sent BOOLEAN NOT NULL DEFAULT false,
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- Add indexes
CREATE INDEX idx_reminder_task ON task_reminders(task_id);
CREATE INDEX idx_reminder_user ON task_reminders(user_id);
CREATE INDEX idx_reminder_pending ON task_reminders(is_sent, remind_at);
CREATE INDEX idx_reminder_user_task ON task_reminders(user_id, task_id);
```

## Query Patterns

### Get Active Tasks for User (Filtered)

```sql
SELECT * FROM tasks
WHERE user_id = :user_id
  AND is_deleted = false
  AND (:status IS NULL OR status = :status)
  AND (:priority IS NULL OR priority = :priority)
  AND (:due_before IS NULL OR due_date <= :due_before)
ORDER BY
    CASE priority
        WHEN 'urgent' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
    END,
    due_date NULLS LAST,
    created_at DESC
LIMIT :limit OFFSET :offset;
```

### Get Pending Reminders

```sql
SELECT r.*, t.title as task_title
FROM task_reminders r
JOIN tasks t ON r.task_id = t.id
WHERE r.is_sent = false
  AND r.remind_at <= now()
ORDER BY r.remind_at ASC;
```

### Mark Task Complete

```sql
UPDATE tasks
SET status = 'completed',
    completed_at = now(),
    updated_at = now()
WHERE id = :task_id
  AND user_id = :user_id
  AND is_deleted = false;
```
