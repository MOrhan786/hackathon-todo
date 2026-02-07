import hashlib
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _normalize_password_sha256(password: str) -> str:
    """
    Normalize password using SHA-256 to avoid bcrypt 72-byte limitation.

    Args:
        password: The plain text password to normalize

    Returns:
        str: The SHA-256 hash of the password as hex string
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def is_legacy_hash(hashed_password: str) -> bool:
    """
    Check if the hash is a legacy hash (direct bcrypt of original password).
    Legacy hashes don't have the 'v2$' prefix that new hashes will have.

    Args:
        hashed_password: The hashed password to check

    Returns:
        bool: True if it's a legacy hash, False otherwise
    """
    return not hashed_password.startswith("v2$")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Supports both legacy hashes and new SHA-256 normalized hashes.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against

    Returns:
        bool: True if the password matches, False otherwise
    """
    if is_legacy_hash(hashed_password):
        # Handle legacy hash (direct bcrypt of original password with 72-byte truncation)
        # Truncate password to 72 bytes to match how it was originally hashed
        password_bytes = plain_password.encode('utf-8')
        truncated_bytes = password_bytes[:72]
        truncated_password = truncated_bytes.decode('utf-8', errors='ignore')
        return pwd_context.verify(truncated_password, hashed_password)
    else:
        # Handle new hash (SHA-256 normalized before bcrypt)
        # Remove the version prefix before verification
        normalized_hash = _normalize_password_sha256(plain_password)
        bcrypt_hash = hashed_password[3:]  # Remove "v2$" prefix
        return pwd_context.verify(normalized_hash, bcrypt_hash)

def get_password_hash(password: str) -> str:
    """
    Hash a password using SHA-256 normalization followed by bcrypt.
    This avoids the bcrypt 72-byte limitation by normalizing any length password
    to a fixed 64-character hex string before bcrypt hashing.

    Args:
        password: The plain text password to hash

    Returns:
        str: The hashed password with version prefix
    """
    normalized_password = _normalize_password_sha256(password)
    bcrypt_hash = pwd_context.hash(normalized_password)
    # Prefix with "v2$" to indicate this is the new hash format
    return f"v2${bcrypt_hash}"

def get_legacy_password_hash(password: str) -> str:
    """
    Hash a password using the legacy method (truncated to 72 bytes before bcrypt).
    This is kept for testing and migration purposes only.

    Args:
        password: The plain text password to hash

    Returns:
        str: The legacy hashed password
    """
    # Truncate password to 72 bytes to avoid bcrypt limitation
    # First encode to bytes, then truncate to 72 bytes, then decode back to string
    password_bytes = password.encode('utf-8')
    truncated_bytes = password_bytes[:72]
    truncated_password = truncated_bytes.decode('utf-8', errors='ignore')
    return pwd_context.hash(truncated_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time for the token

    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid.

    Args:
        token: The JWT token to verify

    Returns:
        Optional[dict]: The token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user_id from a JWT token.

    Args:
        token: The JWT token to extract user_id from

    Returns:
        Optional[str]: The user_id if found and valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        user_id: str = payload.get("sub")
        if user_id:
            return user_id
    return None