"""
Simple pytest configuration for tests that don't need database setup.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    """
    Create a test client for the FastAPI application without database setup.
    """
    # Create a test app instance
    test_app = create_app()
    
    with TestClient(test_app) as test_client:
        yield test_client 