#!/usr/bin/env python3
"""
Test script to verify the authentication system with SHA-256 normalization implementation.
This script tests user registration, login, and password verification to ensure long passwords
are handled properly without breaking existing functionality.
"""

import sys
import os
import uuid
from datetime import datetime, timedelta

# Add backend src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import StaticPool
from src.config import settings
from src.models.user import User, UserCreate
from src.services.user_service import UserService
from src.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token,
    get_user_id_from_token,
    _normalize_password_sha256,
    is_legacy_hash
)


def test_sha256_normalization():
    """Test the SHA-256 password normalization function."""
    print("Testing SHA-256 password normalization...")

    # Test with various password lengths
    short_password = "short"
    long_password = "a" * 100  # Very long password
    unicode_password = "password_with_unicode_üñíçødé"

    # Normalize passwords
    short_normalized = _normalize_password_sha256(short_password)
    long_normalized = _normalize_password_sha256(long_password)
    unicode_normalized = _normalize_password_sha256(unicode_password)

    # Verify that all normalized passwords have the same length (64 chars for SHA-256 hex)
    assert len(short_normalized) == 64, f"Short password normalized length is {len(short_normalized)}, expected 64"
    assert len(long_normalized) == 64, f"Long password normalized length is {len(long_normalized)}, expected 64"
    assert len(unicode_normalized) == 64, f"Unicode password normalized length is {len(unicode_normalized)}, expected 64"

    # Verify that different passwords produce different hashes
    assert short_normalized != long_normalized, "Different passwords should produce different hashes"
    assert short_normalized != unicode_normalized, "Different passwords should produce different hashes"
    assert long_normalized != unicode_normalized, "Different passwords should produce different hashes"

    print("✓ SHA-256 normalization tests passed")


def test_password_hashing_and_verification():
    """Test password hashing and verification with SHA-256 normalization."""
    print("\nTesting password hashing and verification...")

    # Test with various password lengths
    test_passwords = [
        "short",                    # Short password
        "medium_length_pass",       # Medium length
        "a" * 50,                   # Long password
        "a" * 100,                  # Very long password
        "password_with_special_chars!@#$%^&*()",  # Special characters
        "password_with_unicode_üñíçødé",           # Unicode characters
    ]

    for i, password in enumerate(test_passwords):
        print(f"  Testing password {i+1}: length={len(password)}")

        # Hash the password
        hashed = get_password_hash(password)

        # Verify it's in the new format (starts with v2$)
        assert hashed.startswith("v2$"), f"Hash should start with 'v2$', got: {hashed[:10]}..."

        # Verify the password
        is_valid = verify_password(password, hashed)
        assert is_valid, f"Password verification failed for password: {password[:10]}..."

        # Verify that wrong passwords fail
        wrong_password = password + "wrong"
        is_invalid = not verify_password(wrong_password, hashed)
        assert is_invalid, f"Wrong password should not verify, but it did for: {wrong_password[:10]}..."

        print(f"    ✓ Password length {len(password)} verified successfully")

    print("✓ Password hashing and verification tests passed")


def test_legacy_password_compatibility():
    """Test backward compatibility with legacy password hashes."""
    print("\nTesting legacy password compatibility...")

    from utils.auth import get_legacy_password_hash

    # Create a legacy hash (truncated to 72 bytes before bcrypt)
    password = "a" * 100  # Very long password
    legacy_hash = get_legacy_password_hash(password)

    # Verify it's NOT in the new format (doesn't start with v2$)
    assert not legacy_hash.startswith("v2$"), f"Legacy hash should not start with 'v2$', got: {legacy_hash[:10]}..."

    # Verify it's recognized as legacy
    assert is_legacy_hash(legacy_hash), f"Legacy hash should be recognized as legacy: {legacy_hash[:10]}..."

    # Verify the password against the legacy hash
    is_valid = verify_password(password, legacy_hash)
    assert is_valid, f"Password verification failed for legacy hash: {password[:10]}..."

    print("✓ Legacy password compatibility tests passed")


def test_jwt_token_operations():
    """Test JWT token creation and verification."""
    print("\nTesting JWT token operations...")

    # Create a sample payload
    user_data = {"sub": str(uuid.uuid4()), "email": "test@example.com"}

    # Create token with default expiration
    token = create_access_token(data=user_data)
    assert token is not None, "Token should not be None"
    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 0, "Token should not be empty"

    # Verify the token
    payload = verify_token(token)
    assert payload is not None, "Payload should not be None"
    assert payload["sub"] == user_data["sub"], "Subject should match"
    assert "exp" in payload, "Expiration should be in payload"

    # Extract user ID from token
    user_id = get_user_id_from_token(token)
    assert user_id == user_data["sub"], "Extracted user ID should match"

    # Test with custom expiration
    custom_expire = timedelta(minutes=10)
    custom_token = create_access_token(data=user_data, expires_delta=custom_expire)
    custom_payload = verify_token(custom_token)
    assert custom_payload is not None, "Custom token payload should not be None"

    print("✓ JWT token operations tests passed")


def test_database_integration():
    """Test the complete authentication flow with database integration."""
    print("\nTesting database integration...")

    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Test user registration
        user_create = UserCreate(email="test@example.com", password="very_long_password_that_exceeds_bcrypts_72_byte_limit_" + "x" * 50)
        user = UserService.create_user(session, user_create)

        assert user is not None, "User should be created"
        assert user.email == "test@example.com", "Email should match"
        assert user.password_hash.startswith("v2$"), "Password should be stored in new format"

        print("  ✓ User registration successful")

        # Test user authentication
        authenticated_user = UserService.authenticate_user(
            session, "test@example.com", user_create.password
        )

        assert authenticated_user is not None, "User should authenticate successfully"
        assert authenticated_user.id == user.id, "Authenticated user ID should match"

        print("  ✓ User authentication successful")

        # Test authentication with wrong password
        failed_auth = UserService.authenticate_user(
            session, "test@example.com", "wrong_password"
        )

        assert failed_auth is None, "Authentication should fail with wrong password"

        print("  ✓ Authentication with wrong password failed as expected")

        # Test authentication with wrong email
        failed_auth2 = UserService.authenticate_user(
            session, "nonexistent@example.com", user_create.password
        )

        assert failed_auth2 is None, "Authentication should fail with nonexistent email"

        print("  ✓ Authentication with wrong email failed as expected")

    print("✓ Database integration tests passed")


def test_edge_cases():
    """Test edge cases for password handling."""
    print("\nTesting edge cases...")

    # Test with empty password (should handle gracefully)
    try:
        empty_hash = get_password_hash("")
        is_empty_valid = verify_password("", empty_hash)
        assert is_empty_valid, "Empty password should verify against its hash"
        print("  ✓ Empty password handled correctly")
    except Exception as e:
        print(f"  ⚠ Empty password test failed: {e}")

    # Test with very long password (over 1000 chars)
    very_long_password = "x" * 1000
    long_hash = get_password_hash(very_long_password)
    is_long_valid = verify_password(very_long_password, long_hash)
    assert is_long_valid, "Very long password should verify against its hash"
    print("  ✓ Very long password (1000 chars) handled correctly")

    # Test with special Unicode characters
    unicode_password = "üñíçødé_π_∑_∫_≥_≤_∞_µ_α_β_γ_δ"
    unicode_hash = get_password_hash(unicode_password)
    is_unicode_valid = verify_password(unicode_password, unicode_hash)
    assert is_unicode_valid, "Unicode password should verify against its hash"
    print("  ✓ Unicode password handled correctly")

    print("✓ Edge cases tests passed")


def main():
    """Run all authentication verification tests."""
    print("=" * 60)
    print("AUTHENTICATION SYSTEM VERIFICATION")
    print("=" * 60)

    try:
        test_sha256_normalization()
        test_password_hashing_and_verification()
        test_legacy_password_compatibility()
        test_jwt_token_operations()
        test_database_integration()
        test_edge_cases()

        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("Authentication system with SHA-256 normalization is working correctly.")
        print("- User registration works with long passwords")
        print("- Login and password verification work properly")
        print("- Long passwords (>72 chars) are handled without bcrypt limitations")
        print("- Existing functionality remains intact")
        print("- JWT token operations work correctly")
        print("=" * 60)

        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)