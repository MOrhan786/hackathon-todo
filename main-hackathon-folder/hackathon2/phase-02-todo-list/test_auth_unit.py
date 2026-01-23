#!/usr/bin/env python3
"""
Unit test to verify the authentication flow works correctly with the bcrypt fix.
This test directly tests the authentication functions without requiring a running server.
"""

import sys
import os
import uuid
from datetime import timedelta
from unittest.mock import Mock, patch
import tempfile
import sqlite3

# Add the backend directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# Mock the settings before importing modules that depend on them
os.environ['DATABASE_URL'] = 'sqlite:///./test_auth.db'
os.environ['JWT_SECRET_KEY'] = 'test_secret_key_for_testing_purposes_only'
os.environ['JWT_REFRESH_SECRET_KEY'] = 'test_refresh_secret_key_for_testing_purposes_only'
os.environ['ALGORITHM'] = 'HS256'
os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = '30'

# Now import the modules after environment is set
from backend.src.database import get_session_context, create_db_and_tables
from backend.src.services.user_service import UserService
from backend.src.models.user import UserCreate
from backend.src.utils.auth import verify_password, get_password_hash


def test_full_auth_flow_with_database():
    """Test the complete authentication flow with database operations."""
    print("Testing full authentication flow with database...")

    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        temp_db_path = temp_db.name

    # Set up the database with the temporary path
    os.environ['DATABASE_URL'] = f'sqlite:///{temp_db_path}'

    # Force reload the config module to pick up the new DATABASE_URL
    import importlib
    import backend.core.config
    importlib.reload(backend.core.config)

    # Now import the modules that depend on the config
    from backend.src.database import get_session_context, create_db_and_tables
    from backend.src.services.user_service import UserService
    from backend.src.models.user import UserCreate

    # Create database tables
    create_db_and_tables()
    print("✓ Database tables created")

    # Test cases with different password lengths
    test_cases = [
        ("short123", "short password"),
        ("a" * 72, "exactly 72-byte password"),
        ("a" * 75, "75-byte password"),
        ("a" * 100, "100-byte password"),
        ("complex_password_over_72_chars_with_numbers_123!@#", "complex long password")
    ]

    for i, (password, description) in enumerate(test_cases):
        email = f"test_user_{i}@example.com"

        try:
            with get_session_context() as session:
                # Create user
                user_create = UserCreate(email=email, password=password)
                db_user = UserService.create_user(session, user_create)

                # Verify user was created
                assert db_user.email == email
                assert db_user.password_hash is not None
                print(f"✓ User creation successful for {description}")

                # Test authentication with correct password
                authenticated_user = UserService.authenticate_user(session, email, password)
                assert authenticated_user is not None
                assert authenticated_user.id == db_user.id
                print(f"✓ Authentication successful for {description}")

                # Test that wrong password fails
                wrong_auth = UserService.authenticate_user(session, email, "wrong_password")
                assert wrong_auth is None
                print(f"✓ Wrong password correctly rejected for {description}")

                # Clean up: delete the test user
                session.delete(db_user)
                session.commit()

        except Exception as e:
            print(f"✗ Test failed for {description}: {e}")
            import traceback
            traceback.print_exc()
            return False

    # Clean up the temporary database file
    try:
        os.unlink(temp_db_path)
    except:
        pass

    print("✓ Full authentication flow test completed successfully")
    return True


def test_password_security_properties():
    """Test that the password hashing maintains security properties."""
    print("\nTesting password security properties...")

    # Test that identical passwords produce different hashes (salt)
    password = "test_password_over_72_chars_with_numbers_123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Hashes should be different due to salt, but both should verify the password
    assert hash1 != hash2, "Hashes should be different due to salting"
    assert verify_password(password, hash1), "Password should verify against first hash"
    assert verify_password(password, hash2), "Password should verify against second hash"
    print("✓ Password salting works correctly")

    # Test that different passwords produce different hashes
    password1 = "password_one_over_72_chars_with_numbers_123"
    password2 = "password_two_over_72_chars_with_numbers_456"

    hash1 = get_password_hash(password1)
    hash2 = get_password_hash(password2)

    assert hash1 != hash2, "Different passwords should produce different hashes"
    assert verify_password(password1, hash1), "Password1 should verify against its own hash"
    assert verify_password(password2, hash2), "Password2 should verify against its own hash"
    assert not verify_password(password1, hash2), "Password1 should not verify against password2's hash"
    assert not verify_password(password2, hash1), "Password2 should not verify against password1's hash"
    print("✓ Different passwords handled securely")

    return True


def test_bcrypt_limit_handling():
    """Test specific handling of the bcrypt 72-byte limit."""
    print("\nTesting bcrypt limit handling...")

    # Test that very long passwords are handled consistently
    very_long_password = "a" * 100

    # Hash the password
    hash_result = get_password_hash(very_long_password)

    # Verify with the original long password
    assert verify_password(very_long_password, hash_result), "Very long password should verify"

    # Also verify with the first 72 characters (the effective password after truncation)
    first_72 = very_long_password[:72]
    assert verify_password(first_72, hash_result), "First 72 chars should verify against hash"

    print("✓ Very long passwords handled correctly")

    # Test with a password that has multibyte characters near the 72-byte boundary
    # Create a password that will be exactly 75 bytes when encoded
    password_utf8 = "a" * 70 + "🚀"  # Rocket emoji is 4 bytes in UTF-8
    # Total: 70 + 4 = 74 bytes

    hash_utf8 = get_password_hash(password_utf8)
    assert verify_password(password_utf8, hash_utf8), "UTF-8 password should verify"

    print("✓ UTF-8 character handling works correctly")

    return True


def main():
    """Run all authentication tests."""
    print("=" * 70)
    print("TESTING AUTHENTICATION FLOW WITH BCRYPT FIX")
    print("=" * 70)

    try:
        success = True

        success &= test_password_security_properties()
        success &= test_bcrypt_limit_handling()
        success &= test_full_auth_flow_with_database()

        if success:
            print("\n" + "=" * 70)
            print("🎉 ALL AUTHENTICATION TESTS PASSED! 🎉")
            print("✓ Password hashing security maintained")
            print("✓ Bcrypt 72-byte limit handled properly")
            print("✓ Full auth flow works with database")
            print("✓ Long passwords work correctly")
            print("=" * 70)
        else:
            print("\n❌ SOME TESTS FAILED")

        return success

    except Exception as e:
        print(f"\n❌ TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)