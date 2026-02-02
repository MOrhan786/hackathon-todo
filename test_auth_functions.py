#!/usr/bin/env python3
"""
Direct test of the actual auth utility functions to verify the bcrypt 72-byte limit fix.
"""

import sys
import os
# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Mock the settings to avoid needing environment variables
import unittest.mock
from core.config import Settings

mock_settings = Settings(
    DATABASE_URL="sqlite:///./test.db",
    JWT_SECRET_KEY="test_secret_key_for_testing_purposes_only",
    JWT_REFRESH_SECRET_KEY="test_refresh_secret_key_for_testing_purposes_only"
)

with unittest.mock.patch('core.config.settings', mock_settings):
    from utils.auth import get_password_hash, verify_password

def test_actual_auth_functions():
    """Test the actual auth functions in the codebase."""

    print("Testing actual auth utility functions...")

    # Test with a short password (should work normally)
    short_password = "shortpass123"
    short_hash = get_password_hash(short_password)
    assert verify_password(short_password, short_hash), "Short password verification failed"
    print(f"✓ Short password ({len(short_password)} chars) works correctly")

    # Test with a 72-byte password (should work normally)
    password_72_bytes = "a" * 72
    print(f"Creating 72-byte password: {len(password_72_bytes.encode('utf-8'))} bytes")
    password_72_hash = get_password_hash(password_72_bytes)
    assert verify_password(password_72_bytes, password_72_hash), "72-byte password verification failed"
    print(f"✓ 72-byte password ({len(password_72_bytes)} chars) works correctly")

    # Test with a password longer than 72 bytes (should be truncated consistently)
    password_over_72 = "a" * 80  # 80 characters > 72
    print(f"Creating >72-byte password: {len(password_over_72.encode('utf-8'))} bytes")
    password_over_72_hash = get_password_hash(password_over_72)

    # The same password should verify successfully
    assert verify_password(password_over_72, password_over_72_hash), ">72-byte password verification failed"
    print(f"✓ >72-byte password ({len(password_over_72)} chars) works correctly")

    # Most importantly: a different password that differs only after 72 bytes
    # should hash to the same value (because they get truncated to the same 72 bytes)
    password_over_72_variant = "a" * 72 + "different_suffix_that_should_be_truncated"
    print(f"Creating variant >72-byte password: {len(password_over_72_variant.encode('utf-8'))} bytes")

    # Both passwords should verify against the same hash because they're truncated identically
    assert verify_password(password_over_72_variant, password_over_72_hash), "Variant password should verify with original hash (same first 72 bytes)"
    print(f"✓ Variant >72-byte password verifies with original hash (same first 72 bytes)")

    # Test with Unicode characters to make sure byte truncation works correctly
    unicode_password = "ü" * 100  # ü takes 2 bytes in UTF-8, so this will be > 72 bytes
    unicode_bytes = unicode_password.encode('utf-8')
    print(f"Creating Unicode password: {len(unicode_bytes)} bytes ({len(unicode_password)} chars)")

    unicode_hash = get_password_hash(unicode_password)
    assert verify_password(unicode_password, unicode_hash), "Unicode password verification failed"
    print(f"✓ Unicode password ({len(unicode_password)} chars, {len(unicode_bytes)} bytes) works correctly")

    # Test with mixed ASCII and Unicode
    mixed_password = "hello世界" * 20  # Will exceed 72 bytes
    mixed_bytes = mixed_password.encode('utf-8')
    print(f"Creating mixed ASCII/Unicode password: {len(mixed_bytes)} bytes ({len(mixed_password)} chars)")

    mixed_hash = get_password_hash(mixed_password)
    assert verify_password(mixed_password, mixed_hash), "Mixed ASCII/Unicode password verification failed"
    print(f"✓ Mixed ASCII/Unicode password ({len(mixed_password)} chars, {len(mixed_bytes)} bytes) works correctly")

    print("\n🎉 All tests passed! The actual auth utility functions handle the bcrypt 72-byte limit correctly.")
    print("\nAnalysis of the implementation in /mnt/d/main-hackathon-folder/hackathon2/phase-02-todo-list/backend/src/utils/auth.py:")
    print("- ✓ Both get_password_hash() and verify_password() functions implement consistent truncation")
    print("- ✓ Passwords are converted to bytes before truncation to handle Unicode properly")
    print("- ✓ Truncation occurs at exactly 72 bytes to match bcrypt's limitation")
    print("- ✓ Byte truncation is followed by decoding back to string with error handling")
    print("- ✓ The same truncation logic is applied in both functions ensuring consistency")


if __name__ == "__main__":
    test_actual_auth_functions()