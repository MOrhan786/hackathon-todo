from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict
from pydantic import BaseModel
from datetime import datetime, timedelta
from uuid import UUID
from core.db import get_session
from models.user import UserCreate, UserLogin, UserResponse
from services.user_service import UserService
from utils.auth import create_access_token
from core.security import create_access_token as create_jwt_access_token, create_refresh_token, verify_refresh_token

# Response model for registration that includes JWT tokens
class UserRegistrationResponse(BaseModel):
    """Response model for user registration that includes JWT tokens."""
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# router = APIRouter(prefix="/auth", tags=["authentication"])
router = APIRouter(prefix="/auth")



@router.post("/register", response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.

    Args:
        user_create: User registration data
        session: Database session

    Returns:
        UserRegistrationResponse: The created user data with JWT token

    Raises:
        HTTPException: If user already exists
    """
    try:
        # Create the user
        db_user = UserService.create_user(session, user_create)

        # Create access and refresh tokens
        access_token_expires = timedelta(minutes=30)  # Use configurable setting
        access_token = create_jwt_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": str(db_user.id)})

        # Return user data with tokens
        return {
            "id": db_user.id,
            "email": db_user.email,
            "created_at": db_user.created_at,
            "updated_at": db_user.updated_at,
            "access_token": access_token,
            "refresh_token": refresh_token,
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
    Authenticate a user and return JWT tokens.

    Args:
        user_login: User login credentials
        session: Database session

    Returns:
        Dict: Access token, refresh token, user data, and token type

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

    # Create access and refresh tokens
    access_token = create_jwt_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh(refresh_request: Dict[str, str]):
    """
    Refresh access token using refresh token.

    Args:
        refresh_request: Dict containing refresh_token

    Returns:
        Dict: New access token and token type

    Raises:
        HTTPException: If refresh token is invalid
    """
    refresh_token = refresh_request.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required"
        )

    # Verify refresh token
    payload = verify_refresh_token(refresh_token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new access token
    access_token = create_jwt_access_token(data={"sub": user_id})

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