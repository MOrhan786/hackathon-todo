---
name: jwt-middleware-generator
description: "Generate JWT verification middleware. Ensures secure JWT handling for user authentication in chatbot tasks and operations with proper token validation and refresh mechanisms."
version: "1.0.0"
used_by:
  - Full-Stack-Backend
  - Chatbot Authentication Agent
tags:
  - authentication
  - jwt
  - security
  - middleware
---

# JWT Middleware Generator Skill

## Purpose

Generate secure JWT verification middleware for user authentication. This skill ensures proper JWT handling for all application operations including chatbot tasks, with secure token validation, refresh mechanisms, and user context extraction.

## Capabilities

### 1. Token Generation
- Generate access tokens with configurable expiration
- Create refresh tokens for session extension
- Include custom claims (user ID, roles, permissions)
- Support multiple token types (access, refresh, API keys)

### 2. Token Validation Middleware
- Verify token signatures
- Check token expiration
- Validate token claims
- Handle token revocation

### 3. User Context Extraction
- Extract user information from tokens
- Provide user context to request handlers
- Support role-based access control
- Handle guest/anonymous access

### 4. Refresh Token Flow
- Implement secure refresh endpoint
- Handle token rotation
- Manage refresh token families
- Detect token reuse attacks

### 5. Chatbot Authentication
- Authenticate chatbot API requests
- Maintain session context across messages
- Handle anonymous chatbot access
- Support user linking after authentication

## Code Templates

### Configuration
```python
from pydantic_settings import BaseSettings
from datetime import timedelta

class JWTSettings(BaseSettings):
    """JWT configuration settings."""

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Token settings
    TOKEN_TYPE: str = "Bearer"
    TOKEN_URL: str = "/api/auth/token"

    # Security settings
    VERIFY_SIGNATURE: bool = True
    VERIFY_EXP: bool = True
    VERIFY_NBF: bool = True
    VERIFY_IAT: bool = True
    REQUIRE_EXP: bool = True

    class Config:
        env_prefix = "JWT_"

jwt_settings = JWTSettings()
```

### Token Service
```python
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenService:
    """Service for JWT token operations."""

    def __init__(self, settings: JWTSettings):
        self.settings = settings

    def create_access_token(
        self,
        user_id: int,
        email: str,
        roles: list[str] = None,
        additional_claims: Dict[str, Any] = None
    ) -> str:
        """Create a new access token."""
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        claims = {
            "sub": str(user_id),
            "email": email,
            "roles": roles or [],
            "type": "access",
            "exp": expires,
            "iat": datetime.now(timezone.utc),
        }

        if additional_claims:
            claims.update(additional_claims)

        return jwt.encode(
            claims,
            self.settings.SECRET_KEY,
            algorithm=self.settings.ALGORITHM
        )

    def create_refresh_token(
        self,
        user_id: int,
        token_family: str = None
    ) -> str:
        """Create a new refresh token."""
        expires = datetime.now(timezone.utc) + timedelta(
            days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        claims = {
            "sub": str(user_id),
            "type": "refresh",
            "family": token_family or self._generate_family_id(),
            "exp": expires,
            "iat": datetime.now(timezone.utc),
        }

        return jwt.encode(
            claims,
            self.settings.SECRET_KEY,
            algorithm=self.settings.ALGORITHM
        )

    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """Verify and decode a token."""
        try:
            payload = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.ALGORITHM]
            )

            if payload.get("type") != token_type:
                raise JWTError(f"Invalid token type: expected {token_type}")

            return payload

        except jwt.ExpiredSignatureError:
            raise JWTError("Token has expired")
        except jwt.JWTClaimsError as e:
            raise JWTError(f"Invalid claims: {str(e)}")
        except JWTError as e:
            raise JWTError(f"Invalid token: {str(e)}")

    def _generate_family_id(self) -> str:
        """Generate a unique token family ID."""
        import uuid
        return str(uuid.uuid4())

token_service = TokenService(jwt_settings)
```

### FastAPI Middleware
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer(auto_error=False)

class TokenPayload:
    """Validated token payload."""

    def __init__(self, payload: Dict[str, Any]):
        self.user_id = int(payload["sub"])
        self.email = payload.get("email")
        self.roles = payload.get("roles", [])
        self.token_type = payload.get("type")
        self.exp = payload.get("exp")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenPayload:
    """Dependency to get current authenticated user."""

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = token_service.verify_token(credentials.credentials)
        return TokenPayload(payload)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[TokenPayload]:
    """Dependency for optional authentication (allows anonymous)."""

    if not credentials:
        return None

    try:
        payload = token_service.verify_token(credentials.credentials)
        return TokenPayload(payload)
    except JWTError:
        return None

def require_roles(*required_roles: str):
    """Dependency factory for role-based access control."""

    async def role_checker(
        user: TokenPayload = Depends(get_current_user)
    ) -> TokenPayload:
        for role in required_roles:
            if role not in user.roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Required role: {role}"
                )
        return user

    return role_checker
```

### Auth Endpoints
```python
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return tokens."""

    user = await get_user_by_email(db, request.email)

    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    access_token = token_service.create_access_token(
        user_id=user.id,
        email=user.email,
        roles=["user"]  # Get from user model
    )

    refresh_token = token_service.create_refresh_token(user_id=user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshRequest):
    """Refresh access token using refresh token."""

    try:
        payload = token_service.verify_token(
            request.refresh_token,
            token_type="refresh"
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    # Create new tokens
    access_token = token_service.create_access_token(
        user_id=int(payload["sub"]),
        email=payload.get("email", ""),
        roles=payload.get("roles", [])
    )

    # Rotate refresh token
    new_refresh_token = token_service.create_refresh_token(
        user_id=int(payload["sub"]),
        token_family=payload.get("family")
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/logout")
async def logout(user: TokenPayload = Depends(get_current_user)):
    """Logout current user (invalidate tokens)."""
    # Add token to blacklist or invalidate refresh token family
    return {"message": "Successfully logged out"}
```

### Chatbot Authentication
```python
class ChatbotAuthMiddleware:
    """Authentication for chatbot requests."""

    async def authenticate_chatbot_request(
        self,
        credentials: Optional[HTTPAuthorizationCredentials],
        session_id: Optional[str] = None
    ) -> Optional[TokenPayload]:
        """
        Authenticate chatbot request.
        Supports both authenticated users and anonymous sessions.
        """

        if credentials:
            try:
                payload = token_service.verify_token(credentials.credentials)
                return TokenPayload(payload)
            except JWTError:
                pass

        # Allow anonymous chatbot access with session tracking
        return None

    def get_chatbot_context(
        self,
        user: Optional[TokenPayload],
        session_id: str
    ) -> Dict[str, Any]:
        """Build context for chatbot operations."""

        return {
            "is_authenticated": user is not None,
            "user_id": user.user_id if user else None,
            "session_id": session_id,
            "can_manage_tasks": user is not None,
            "permissions": user.roles if user else []
        }
```

## Security Best Practices

### Token Security
- Use strong secret keys (min 256 bits)
- Set appropriate expiration times
- Implement token rotation for refresh tokens
- Store refresh tokens securely (httpOnly cookies)

### Request Security
- Always use HTTPS in production
- Validate token on every protected request
- Implement rate limiting on auth endpoints
- Log authentication events for monitoring

### Error Handling
- Never expose sensitive information in errors
- Use generic error messages for auth failures
- Implement account lockout after failed attempts
- Monitor for suspicious authentication patterns

## Usage Examples

### Protect API Endpoint
```python
@router.get("/tasks")
async def get_tasks(user: TokenPayload = Depends(get_current_user)):
    # user is guaranteed to be authenticated
    return await task_service.get_user_tasks(user.user_id)
```

### Optional Authentication
```python
@router.get("/public-tasks")
async def get_public_tasks(user: Optional[TokenPayload] = Depends(get_optional_user)):
    if user:
        return await task_service.get_user_and_public_tasks(user.user_id)
    return await task_service.get_public_tasks()
```

### Role-Based Access
```python
@router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: TokenPayload = Depends(require_roles("admin"))
):
    return await user_service.delete_user(user_id)
```

## Integration Points

- Works with SQLModel-Schema-Generator for user models
- Integrates with FastAPI-Endpoint-Generator for protected routes
- Coordinates with JWT-Auth-Manager agent for complex flows
- Feeds into Chatbot authentication system
