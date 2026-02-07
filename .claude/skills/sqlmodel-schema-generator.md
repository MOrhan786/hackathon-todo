---
name: sqlmodel-schema-generator
description: "Create optimized SQLModel models with indexes. Ensures optimized data storage for tasks, user information, and chatbot interactions with proper relationships and constraints."
version: "1.0.0"
used_by:
  - Full-Stack-Backend
  - Chatbot Data Manager
tags:
  - database
  - sqlmodel
  - schema
  - optimization
---

# SQLModel Schema Generator Skill

## Purpose

Create optimized SQLModel models with proper indexes, relationships, and constraints. This skill ensures efficient data storage for tasks, user information, and chatbot interactions with optimal query performance.

## Capabilities

### 1. Model Definition
- Generate SQLModel class definitions
- Define field types with proper constraints
- Set up primary keys and foreign keys
- Configure nullable and default values

### 2. Index Optimization
- Create indexes for frequently queried fields
- Design composite indexes for complex queries
- Optimize for common access patterns
- Balance read vs write performance

### 3. Relationship Mapping
- Define one-to-many relationships
- Configure many-to-many with junction tables
- Set up cascading behaviors
- Handle self-referential relationships

### 4. Task Management Schema
- Design task model with all attributes
- Create task categories and tags
- Handle recurring task patterns
- Support task history and audit trails

### 5. Chatbot Data Schema
- Design conversation session models
- Create message history tables
- Store intent and entity data
- Handle user preferences and context

## Model Templates

### User Model
```python
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Index

class User(SQLModel, table=True):
    """User account model with authentication support."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    chat_sessions: List["ChatSession"] = Relationship(back_populates="user")

    __table_args__ = (
        Index("idx_user_email_active", "email", "is_active"),
    )
```

### Task Model
```python
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Task(SQLModel, table=True):
    """Task model with full feature support."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255, index=True)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, index=True)
    due_date: Optional[datetime] = Field(default=None, index=True)
    completed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Recurring task support
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None)
    parent_task_id: Optional[int] = Field(
        default=None,
        foreign_key="tasks.id"
    )

    # Soft delete
    is_deleted: bool = Field(default=False, index=True)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")
    tags: List["TaskTag"] = Relationship(back_populates="task")
    reminders: List["TaskReminder"] = Relationship(back_populates="task")

    __table_args__ = (
        Index("idx_task_user_status", "user_id", "status"),
        Index("idx_task_user_due", "user_id", "due_date"),
        Index("idx_task_user_priority", "user_id", "priority"),
        Index("idx_task_active", "user_id", "is_deleted", "status"),
    )
```

### Task Tag Model
```python
class Tag(SQLModel, table=True):
    """Tag/category for organizing tasks."""

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=50)
    color: Optional[str] = Field(default=None, max_length=7)

    __table_args__ = (
        Index("idx_tag_user_name", "user_id", "name", unique=True),
    )

class TaskTag(SQLModel, table=True):
    """Junction table for task-tag many-to-many."""

    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)

    task: "Task" = Relationship(back_populates="tags")
    tag: "Tag" = Relationship()
```

### Task Reminder Model
```python
class TaskReminder(SQLModel, table=True):
    """Reminder notifications for tasks."""

    __tablename__ = "task_reminders"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id", index=True)
    remind_at: datetime = Field(index=True)
    is_sent: bool = Field(default=False, index=True)
    sent_at: Optional[datetime] = Field(default=None)

    task: "Task" = Relationship(back_populates="reminders")

    __table_args__ = (
        Index("idx_reminder_pending", "remind_at", "is_sent"),
    )
```

### Chatbot Session Model
```python
class ChatSession(SQLModel, table=True):
    """Chatbot conversation session."""

    __tablename__ = "chat_sessions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True, index=True)

    # Context storage
    context_data: Optional[str] = Field(default=None)  # JSON

    # Relationships
    user: "User" = Relationship(back_populates="chat_sessions")
    messages: List["ChatMessage"] = Relationship(back_populates="session")

    __table_args__ = (
        Index("idx_session_user_active", "user_id", "is_active"),
    )

class ChatMessage(SQLModel, table=True):
    """Individual chatbot message."""

    __tablename__ = "chat_messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="chat_sessions.id", index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str
    intent: Optional[str] = Field(default=None, max_length=50)
    entities: Optional[str] = Field(default=None)  # JSON
    created_at: datetime = Field(default_factory=datetime.utcnow)

    session: "ChatSession" = Relationship(back_populates="messages")

    __table_args__ = (
        Index("idx_message_session_time", "session_id", "created_at"),
    )
```

## Index Strategy

### Query Pattern Analysis
```yaml
common_queries:
  get_user_tasks:
    query: "SELECT * FROM tasks WHERE user_id = ? AND is_deleted = false"
    index: idx_task_active (user_id, is_deleted, status)

  get_tasks_by_due_date:
    query: "SELECT * FROM tasks WHERE user_id = ? AND due_date BETWEEN ? AND ?"
    index: idx_task_user_due (user_id, due_date)

  get_pending_reminders:
    query: "SELECT * FROM task_reminders WHERE remind_at <= ? AND is_sent = false"
    index: idx_reminder_pending (remind_at, is_sent)

  search_tasks:
    query: "SELECT * FROM tasks WHERE user_id = ? AND title ILIKE ?"
    index: idx_task_user_status + full-text search
```

### Index Recommendations
```yaml
index_strategy:
  primary_indexes:
    - All foreign keys (automatic query joins)
    - Frequently filtered columns (status, is_deleted)

  composite_indexes:
    - Combine user_id with common filters
    - Order by selectivity (most selective first)

  partial_indexes:
    - Active tasks only (WHERE is_deleted = false)
    - Pending reminders (WHERE is_sent = false)

  avoid:
    - Indexes on low-cardinality columns alone
    - Too many indexes on write-heavy tables
```

## Usage Examples

### Generate Task Schema
```
Input: Create task model with priorities, due dates, and recurring support

Output:
- Task model with all fields
- TaskStatus and TaskPriority enums
- Indexes for common queries
- Relationships to user and tags
```

### Generate Chatbot Schema
```
Input: Create schema for chatbot conversation storage

Output:
- ChatSession model
- ChatMessage model with intent/entities
- Indexes for session queries
- Context data storage
```

## Migration Support

### Alembic Migration Template
```python
"""Add task priority index

Revision ID: abc123
Revises: xyz789
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_index(
        'idx_task_user_priority',
        'tasks',
        ['user_id', 'priority'],
        unique=False
    )

def downgrade():
    op.drop_index('idx_task_user_priority', table_name='tasks')
```

## Integration Points

- Works with JWT-Middleware-Generator for user authentication
- Feeds into FastAPI-Endpoint-Generator for API design
- Coordinates with Neon-Postgres-DBA agent for optimization
- Integrates with Task-Coordinator agent for query patterns
