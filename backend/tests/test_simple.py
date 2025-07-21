"""
Simple tests that don't require database setup.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from tests.conftest_simple import client


def test_app_creation():
    """Test that the app can be created."""
    app = create_app()
    assert app is not None
    assert app.title == "GoodStewards API"


def test_app_routes():
    """Test that the app has the expected routes."""
    app = create_app()
    
    # Test basic endpoints directly
    with TestClient(app) as client:
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200
        
        # Test health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        
        # Test API info endpoint
        response = client.get("/api/v1/")
        assert response.status_code == 200


def test_app_docs_routes():
    """Test that documentation routes exist."""
    app = create_app()
    
    with TestClient(app) as client:
        # Test OpenAPI docs
        response = client.get("/api/v1/docs")
        assert response.status_code == 200
        
        # Test OpenAPI JSON
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        
        # Test ReDoc
        response = client.get("/api/v1/redoc")
        assert response.status_code == 200


def test_app_api_routes():
    """Test that API routes exist."""
    app = create_app()
    
    with TestClient(app) as client:
        # Test auth endpoints exist (should return 401 or 422, not 404)
        response = client.get("/api/v1/auth/me")
        assert response.status_code in [401, 422]  # Not 404
        
        # Test receipt endpoints exist (should return 401 or 422, not 404)
        response = client.get("/api/v1/receipts/")
        assert response.status_code in [401, 422]  # Not 404 