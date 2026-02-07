import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from jose import jwt
from core.config import settings


class TestAuthentication:
    """Test suite for authentication endpoints."""

    def test_register_success(self, client: TestClient):
        """Test successful user registration."""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "securePassword123!"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["email"] == "test@example.com"

    def test_register_duplicate_email(self, client: TestClient):
        """Test registration with duplicate email."""
        # First registration
        client.post(
            "/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )
        # Second registration with same email
        response = client.post(
            "/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password456"
            }
        )
        assert response.status_code == 409

    def test_login_success(self, client: TestClient):
        """Test successful login."""
        # Register user
        client.post(
            "/auth/register",
            json={
                "email": "login@example.com",
                "password": "password123"
            }
        )
        # Login
        response = client.post(
            "/auth/login",
            json={
                "email": "login@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials."""
        response = client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401

    def test_access_token_expiry(self, client: TestClient):
        """Test that access token has correct expiry time (60 minutes)."""
        # Register and get token
        response = client.post(
            "/auth/register",
            json={
                "email": "expiry@example.com",
                "password": "password123"
            }
        )
        access_token = response.json()["access_token"]

        # Decode token and check expiry
        payload = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        now = datetime.utcnow()

        # Should be approximately 60 minutes (allow 1 minute tolerance)
        time_diff = (exp_datetime - now).total_seconds() / 60
        assert 59 <= time_diff <= 61

    def test_refresh_token_success(self, client: TestClient):
        """Test successful token refresh."""
        # Register and get tokens
        response = client.post(
            "/auth/register",
            json={
                "email": "refresh@example.com",
                "password": "password123"
            }
        )
        refresh_token = response.json()["refresh_token"]

        # Use refresh token to get new access token
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_token_invalid(self, client: TestClient):
        """Test refresh with invalid token."""
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": "invalid.token.here"}
        )
        assert response.status_code == 401

    def test_protected_endpoint_without_token(self, client: TestClient):
        """Test accessing protected endpoint without token."""
        response = client.get("/api/tasks")
        assert response.status_code == 401

    def test_protected_endpoint_with_valid_token(self, client: TestClient):
        """Test accessing protected endpoint with valid token."""
        # Register and get token
        response = client.post(
            "/auth/register",
            json={
                "email": "protected@example.com",
                "password": "password123"
            }
        )
        access_token = response.json()["access_token"]

        # Access protected endpoint
        response = client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200

    def test_protected_endpoint_with_expired_token(self, client: TestClient):
        """Test accessing protected endpoint with expired token."""
        # Create an expired token
        expired_payload = {
            "sub": "test-user-id",
            "exp": datetime.utcnow() - timedelta(minutes=1)
        }
        expired_token = jwt.encode(expired_payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

        # Try to access protected endpoint
        response = client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
