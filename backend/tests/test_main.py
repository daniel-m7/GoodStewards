"""
Tests for main application endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from tests.conftest import client_no_db


def test_read_root(client_no_db: TestClient):
    """Test the root endpoint."""
    response = client_no_db.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert data["message"] == "Welcome to the GoodStewards API"


def test_health_check(client_no_db: TestClient):
    """Test the health check endpoint."""
    response = client_no_db.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_api_info(client_no_db: TestClient):
    """Test the API information endpoint."""
    response = client_no_db.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert "api_version" in data
    assert "endpoints" in data
    assert data["api_version"] == "v1"
    
    # Check that all expected endpoints are listed
    expected_endpoints = [
        "auth", "users", "organizations", "receipts", 
        "forms", "payments"
    ]
    for endpoint in expected_endpoints:
        assert endpoint in data["endpoints"]


def test_openapi_docs(client_no_db: TestClient):
    """Test that OpenAPI documentation is accessible."""
    response = client_no_db.get("/api/v1/docs")
    assert response.status_code == 200


def test_openapi_json(client_no_db: TestClient):
    """Test that OpenAPI JSON schema is accessible."""
    response = client_no_db.get("/api/v1/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data 