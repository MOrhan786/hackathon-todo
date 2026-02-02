# Data Model: Todo Application Backend

## User Entity

```python
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255, index=True)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to todos
    # todos: List["Todo"] = Relationship(back_populates="user")
```

## Todo Entity

```python
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime

class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    # user: Optional[User] = Relationship(back_populates="todos")
```

## Notes

- Primary keys use UUID for better security and distribution
- Email is unique and indexed for fast lookups
- user_id is indexed for efficient filtering by user
- Timestamps are automatically managed
- Passwords must be hashed before storage