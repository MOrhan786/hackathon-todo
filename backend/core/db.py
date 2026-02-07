from sqlmodel import create_engine, Session
from contextlib import contextmanager
from typing import Generator
import os
# from config import settings
from core.config import settings



# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    # Enable connection pooling
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.

    Yields:
        Session: A SQLModel database session
    """
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_context():
    """
    Context manager for database sessions.

    Ensures the session is properly closed after use.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_db_and_tables():
    """
    Create database tables.

    This function should be called on application startup.
    """
    from models.task import Task  # Import here to avoid circular imports
    from models.user import User  # Import User model for database tables
    from models.reminder import TaskReminder  # Import TaskReminder model
    from models.conversation import Conversation  # Import Conversation model
    from models.message import Message  # Import Message model
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)