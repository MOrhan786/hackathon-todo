from typing import Optional
from sqlmodel import Session, select
from models.user import User, UserCreate
from utils.auth import get_password_hash, verify_password
from uuid import UUID
from datetime import datetime


class UserService:
    """Service class for user-related operations."""

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email.

        Args:
            session: Database session
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_id(session: Session, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            session: Database session
            user_id: User's UUID

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """
        Create a new user.

        Args:
            session: Database session
            user_create: User creation data

        Returns:
            Created User object
        """
        # Check if user already exists
        existing_user = UserService.get_user_by_email(session, user_create.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash the password - the get_password_hash function handles bcrypt's 72-byte limit
        hashed_password = get_password_hash(user_create.password)

        # Create the user object
        db_user = User(
            email=user_create.email,
            password_hash=hashed_password
        )

        # Add to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            session: Database session
            email: User's email address
            password: Plain text password

        Returns:
            User object if authentication succeeds, None otherwise
        """
        user = UserService.get_user_by_email(session, email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def update_user(session: Session, user_id: UUID, email: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
        """
        Update a user's information.

        Args:
            session: Database session
            user_id: User's UUID
            email: New email (optional)
            password: New password (optional)

        Returns:
            Updated User object if successful, None if user not found
        """
        user = UserService.get_user_by_id(session, user_id)
        if not user:
            return None

        if email is not None:
            user.email = email
        if password is not None:
            user.password_hash = get_password_hash(password)

        user.updated_at = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def delete_user(session: Session, user_id: UUID) -> bool:
        """
        Delete a user.

        Args:
            session: Database session
            user_id: User's UUID

        Returns:
            True if deletion was successful, False if user not found
        """
        user = UserService.get_user_by_id(session, user_id)
        if not user:
            return False

        session.delete(user)
        session.commit()
        return True