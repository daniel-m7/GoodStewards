"""
Pytest configuration and fixtures for GoodStewards backend tests.
"""
import asyncio
import pytest
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.db import get_session
from app.core.config import settings


# Test database URL - use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client() -> Generator:
    """
    Create a test client for the FastAPI application.
    """
    # Override the database URL for testing
    import os
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    
    # Create a test app instance
    from app.main import create_app
    test_app = create_app()
    
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def client_no_db() -> Generator:
    """
    Create a test client for the FastAPI application without database requirements.
    """
    # Use a dummy database URL that won't cause initialization issues
    import os
    os.environ["DATABASE_URL"] = "sqlite:///./test_no_db.db"
    
    # Create a test app instance
    from app.main import create_app
    test_app = create_app()
    
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def sample_organization_data():
    """Sample organization data for testing."""
    return {
        "name": "Test Nonprofit",
        "fein": "12-3456789",
        "ntee_code": "A01",
        "address": "123 Test St",
        "city": "Test City",
        "state": "NC",
        "zip_code": "12345"
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123",
        "role": "member"
    }


@pytest.fixture
def sample_receipt_data():
    """Sample receipt data for testing."""
    return {
        "vendor_name": "Test Store",
        "purchase_date": "2023-01-15",
        "county": "Wake",
        "subtotal_amount": 50.00,
        "tax_amount": 5.75,
        "total_amount": 55.75,
        "expense_category": "Food",
        "is_donation": False
    } 