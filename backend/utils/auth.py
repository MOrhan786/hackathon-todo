import hashlib
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from core.config import settings


def _normalize_password_sha256(password: str) -> bytes:
    """
    Normalize password using SHA-256 to avoid bcrypt 72-byte limitation.
    Returns bytes ready for bcrypt.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8')


def is_legacy_hash(hashed_password: str) -> bool:
    """
    Check if the hash is a legacy hash (direct bcrypt of original password).
    Legacy hashes don't have the 'v2$' prefix that new hashes will have.
    """
    return not hashed_password.startswith("v2$")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Supports both legacy hashes and new SHA-256 normalized hashes.
    """
    try:
        if is_legacy_hash(hashed_password):
            # Handle legacy hash - truncate to 72 bytes
            password_bytes = plain_password.encode('utf-8')[:72]
            return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
        else:
            # Handle new hash (SHA-256 normalized before bcrypt)
            normalized = _normalize_password_sha256(plain_password)
            bcrypt_hash = hashed_password[3:]  # Remove "v2$" prefix
            return bcrypt.checkpw(normalized, bcrypt_hash.encode('utf-8'))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using SHA-256 normalization followed by bcrypt.
    This avoids the bcrypt 72-byte limitation by normalizing any length password
    to a fixed 64-character hex string before bcrypt hashing.
    """
    normalized = _normalize_password_sha256(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(normalized, salt)
    # Prefix with "v2$" to indicate this is the new hash format
    return f"v2${hashed.decode('utf-8')}"


def get_legacy_password_hash(password: str) -> str:
    """
    Hash a password using the legacy method (truncated to 72 bytes before bcrypt).
    This is kept for testing and migration purposes only.
    """
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
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
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user_id from a JWT token.
    """
    payload = verify_token(token)
    if payload:
        user_id: str = payload.get("sub")
        if user_id:
            return user_id
    return None
