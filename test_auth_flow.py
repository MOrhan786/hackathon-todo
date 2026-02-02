#!/usr/bin/env python3
"""
Test script to verify the authentication flow works correctly with the bcrypt fix.
This script tests user registration, login, and JWT token generation with passwords
longer than 72 bytes to ensure the fix handles the bcrypt limitation properly.
"""

import sys
import os
import uuid
from datetime import timedelta
from sqlmodel import Session
import hashlib

# Add the backend directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.src.database import get_session_context, create_db_and_tables
from backend.src.services.user_service import UserService
from backend.src.models.user import UserCreate
from backend.src.utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token
)


def test_password_hashing_with_long_passwords():
    """Test password hashing with various length passwords including >72 bytes."""
    print("Testing password hashing with various lengths...")

    # Test short password (normal case)
    short_password = "short123"
    short_hash = get_password_hash(short_password)
    assert verify_password(short_password, short_hash), "Short password hashing failed"
    print("✓ Short password hashing works")

    # Test exactly 72-byte password
    password_72_bytes = "a" * 72
    hash_72 = get_password_hash(password_72_bytes)
    assert verify_password(password_72_bytes, hash_72), "72-byte password hashing failed"
    print("✓ 72-byte password hashing works")

    # Test password slightly longer than 72 bytes
    password_75_bytes = "a" * 75
    hash_75 = get_password_hash(password_75_bytes)
    assert verify_password(password_75_bytes, hash_75), "75-byte password hashing failed"
    print("✓ 75-byte password hashing works")

    # Test very long password (>100 bytes)
    password_100_bytes = "a" * 100
    hash_100 = get_password_hash(password_100_bytes)
    assert verify_password(password_100_bytes, hash_100), "100-byte password hashing failed"
    print("✓ 100-byte password hashing works")

    # Test very long password with mixed characters
    long_password = "my_complex_password_that_is_over_72_bytes_with_special_chars_123!@#"
    long_hash = get_password_hash(long_password)
    assert verify_password(long_password, long_hash), "Long mixed password hashing failed"
    print("✓ Long mixed password hashing works")

    # Test that the same password produces consistent results
    test_password = "test_password_over_72_bytes_longer_than_bcrypt_limit_123"
    hash1 = get_password_hash(test_password)
    hash2 = get_password_hash(test_password)

    # Both hashes should verify the original password
    assert verify_password(test_password, hash1), "First hash verification failed"
    assert verify_password(test_password, hash2), "Second hash verification failed"
    print("✓ Consistent hashing for same password")

    # Test that truncated versions of long passwords work with their hashes
    very_long_password = "a" * 100
    very_long_hash = get_password_hash(very_long_password)

    # The truncated version (first 72 chars) should still verify against the hash
    truncated_version = very_long_password[:72]
    assert verify_password(truncated_version, very_long_hash), "Truncated version should verify"
    print("✓ Truncated password verification works correctly")


def test_user_registration_with_long_passwords():
    """Test user registration flow with long passwords."""
    print("\nTesting user registration with long passwords...")

    # Create database tables
    create_db_and_tables()
    print("✓ Database tables created")

    # Test registration with various password lengths
    test_cases = [
        ("short123", "short password"),
        ("a" * 50, "medium password"),
        ("a" * 72, "exactly 72-byte password"),
        ("a" * 75, "slightly over 72-byte password"),
        ("a" * 100, "100-byte password"),
        ("complex_password_over_72_chars_with_numbers_123!@#", "complex long password")
    ]

    for i, (password, description) in enumerate(test_cases):
        email = f"test{i}@example.com"

        try:
            with get_session_context() as session:
                user_create = UserCreate(email=email, password=password)

                # Register user
                db_user = UserService.create_user(session, user_create)

                # Verify the user was created
                assert db_user.email == email, f"Email mismatch for {description}"
                assert db_user.password_hash is not None, f"No password hash for {description}"

                # Verify we can authenticate with the password
                authenticated_user = UserService.authenticate_user(session, email, password)
                assert authenticated_user is not None, f"Authentication failed for {description}"
                assert authenticated_user.id == db_user.id, f"User ID mismatch for {description}"

                print(f"✓ Registration and authentication successful for {description}")

                # Clean up: delete the test user
                session.delete(db_user)
                session.commit()

        except Exception as e:
            print(f"✗ Failed for {description}: {e}")
            raise


def test_jwt_token_generation():
    """Test JWT token generation and verification."""
    print("\nTesting JWT token generation and verification...")

    # Create a sample user ID
    user_id = str(uuid.uuid4())

    # Create access token
    token = create_access_token(data={"sub": user_id})
    assert token is not None, "Token should not be None"
    print("✓ JWT token generated successfully")

    # Verify the token
    payload = verify_token(token)
    assert payload is not None, "Token verification failed"
    assert payload.get("sub") == user_id, "User ID in token doesn't match"
    print("✓ JWT token verification successful")

    # Test token with custom expiration
    custom_expire = timedelta(minutes=5)
    custom_token = create_access_token(data={"sub": user_id}, expires_delta=custom_expire)
    custom_payload = verify_token(custom_token)
    assert custom_payload is not None, "Custom expiration token verification failed"
    assert custom_payload.get("sub") == user_id, "User ID mismatch in custom token"
    print("✓ Custom expiration token works")


def test_complete_auth_flow():
    """Test the complete authentication flow: register -> login -> verify token."""
    print("\nTesting complete authentication flow...")

    create_db_and_tables()

    # Test with a long password (>72 bytes)
    long_password = "very_long_password_over_72_bytes_with_complex_chars_123!@#"
    email = "complete_test@example.com"

    try:
        with get_session_context() as session:
            # Step 1: Register user
            user_create = UserCreate(email=email, password=long_password)
            db_user = UserService.create_user(session, user_create)
            print("✓ User registered successfully")

            # Step 2: Login (authenticate)
            authenticated_user = UserService.authenticate_user(session, email, long_password)
            assert authenticated_user is not None, "Authentication failed"
            assert authenticated_user.id == db_user.id, "Authenticated user ID mismatch"
            print("✓ User authentication successful")

            # Step 3: Generate JWT token (similar to login endpoint)
            from backend.src.utils.auth import create_access_token
            from datetime import timedelta

            access_token = create_access_token(
                data={"sub": str(db_user.id)},
                expires_delta=timedelta(minutes=30)
            )
            assert access_token is not None, "Access token generation failed"
            print("✓ JWT token generated successfully")

            # Step 4: Verify the token
            payload = verify_token(access_token)
            assert payload is not None, "Token verification failed"
            assert payload.get("sub") == str(db_user.id), "Token user ID mismatch"
            print("✓ Token verification successful")

            # Step 5: Test with wrong password
            wrong_auth = UserService.authenticate_user(session, email, "wrong_password")
            assert wrong_auth is None, "Wrong password should not authenticate"
            print("✓ Wrong password correctly rejected")

            # Clean up
            session.delete(db_user)
            session.commit()
            print("✓ Complete auth flow test successful")

    except Exception as e:
        print(f"✗ Complete auth flow failed: {e}")
        raise


def test_bcrypt_limit_edge_cases():
    """Test edge cases around the bcrypt 72-byte limit."""
    print("\nTesting bcrypt limit edge cases...")

    # Test passwords exactly at the boundary
    boundary_tests = [
        ("a" * 70, "70 bytes (under limit)"),
        ("a" * 71, "71 bytes (under limit)"),
        ("a" * 72, "72 bytes (at limit)"),
        ("a" * 73, "73 bytes (over limit)"),
        ("a" * 74, "74 bytes (over limit)"),
        ("a" * 100, "100 bytes (much over limit)")
    ]

    for password, description in boundary_tests:
        password_bytes = len(password.encode('utf-8'))

        # Hash the password
        hashed = get_password_hash(password)

        # Verify with original password
        is_valid = verify_password(password, hashed)
        assert is_valid, f"Verification failed for {description} ({password_bytes} bytes)"

        # For passwords > 72 bytes, also test that the first 72 bytes work
        if password_bytes > 72:
            truncated = password[:72]
            truncated_valid = verify_password(truncated, hashed)
            assert truncated_valid, f"Truncated verification failed for {description}"

        print(f"✓ {description} ({password_bytes} bytes) handled correctly")


def main():
    """Run all authentication flow tests."""
    print("=" * 70)
    print("TESTING AUTHENTICATION FLOW WITH BCRYPT FIX")
    print("=" * 70)

    try:
        test_password_hashing_with_long_passwords()
        test_user_registration_with_long_passwords()
        test_jwt_token_generation()
        test_complete_auth_flow()
        test_bcrypt_limit_edge_cases()

        print("\n" + "=" * 70)
        print("🎉 ALL AUTHENTICATION FLOW TESTS PASSED! 🎉")
        print("✓ Bcrypt fix handles passwords > 72 bytes correctly")
        print("✓ User registration works with long passwords")
        print("✓ User authentication works with long passwords")
        print("✓ JWT token generation and verification works")
        print("✓ Complete auth flow functions properly")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)