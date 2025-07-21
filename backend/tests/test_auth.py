"""
Tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from tests.conftest import client_no_db


def test_auth_login_endpoint_exists(client_no_db: TestClient):
    """Test that the auth login endpoint exists."""
    response = client_no_db.post("/api/v1/auth/login")
    # Should return 422 (validation error) rather than 404 (not found)
    assert response.status_code in [422, 401]


def test_auth_register_endpoint_exists(client_no_db: TestClient):
    """Test that the auth register endpoint exists."""
    response = client_no_db.post("/api/v1/auth/register")
    # Should return 422 (validation error) rather than 404 (not found)
    assert response.status_code in [422, 401]


def test_auth_me_endpoint_exists(client_no_db: TestClient):
    """Test that the auth me endpoint exists."""
    response = client_no_db.get("/api/v1/auth/me")
    # Should return 401 (unauthorized) rather than 404 (not found)
    assert response.status_code == 401


def test_auth_endpoints_require_authentication(client_no_db: TestClient):
    """Test that auth endpoints require authentication."""
    # Test /auth/me without authentication
    response = client_no_db.get("/api/v1/auth/me")
    assert response.status_code == 401
    
    # Test /users/me without authentication
    response = client_no_db.get("/api/v1/users/me")
    assert response.status_code == 401 