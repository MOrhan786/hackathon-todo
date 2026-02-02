from sqlmodel import create_engine, Session
from contextlib import contextmanager
from core.config import settings
from typing import Generator

# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL debug logging
    pool_pre_ping=True  # Verify connections before use
)

def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection.

    Yields:
        Session: A SQLModel database session
    """
    with Session(engine) as session:
        yield session

@contextmanager
def get_session_context():
    """
    Context manager for database sessions.

    Usage:
        with get_session_context() as session:
            # Use session here
            pass
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
    """Create database tables."""
    from ..models.user import User
    from ..models.task import Task  # Using Task instead of Todo for consistency
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)