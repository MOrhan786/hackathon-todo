from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict
from ..database import get_session
from ..models.user import UserCreate, UserLogin, UserResponse
from ..services.user_service import UserService
from ..utils.auth import create_access_token
from datetime import timedelta
from uuid import UUID

# router = APIRouter(prefix="/auth", tags=["authentication"])
router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.

    Args:
        user_create: User registration data
        session: Database session

    Returns:
        UserResponse: The created user data with JWT token

    Raises:
        HTTPException: If user already exists
    """
    try:
        # Create the user
        db_user = UserService.create_user(session, user_create)

        # Create access token
        access_token_expires = timedelta(minutes=30)  # Use configurable setting
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )

        # Return user data with token
        user_response = UserResponse(
            id=db_user.id,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

        return {
            "id": user_response.id,
            "email": user_response.email,
            "created_at": user_response.created_at,
            "updated_at": user_response.updated_at,
            "access_token": access_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        # User already exists
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login")
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate a user and return JWT token.

    Args:
        user_login: User login credentials
        session: Database session

    Returns:
        Dict: Access token and token type

    Raises:
        HTTPException: If credentials are invalid
    """
    user = UserService.authenticate_user(
        session, user_login.email, user_login.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout():
    """
    Logout user (currently just a placeholder - in a real app,
    you might want to implement token blacklisting).

    Returns:
        Dict: Success message
    """
    # In a real application, you might want to implement token blacklisting
    # For now, we just return a success message
    return {"message": "Successfully logged out"}