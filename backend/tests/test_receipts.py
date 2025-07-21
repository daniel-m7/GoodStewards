"""
Tests for receipt endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from tests.conftest import client_no_db


def test_receipts_endpoints_exist(client_no_db: TestClient):
    """Test that receipt endpoints exist."""
    # Test GET /receipts/ without authentication
    response = client_no_db.get("/api/v1/receipts/")
    assert response.status_code == 401  # Should require authentication
    
    # Test GET /receipts/{receipt_id} without authentication
    response = client_no_db.get("/api/v1/receipts/test-receipt-id")
    assert response.status_code == 401  # Should require authentication
    
    # Test POST /receipts/upload without authentication
    response = client_no_db.post("/api/v1/receipts/upload")
    assert response.status_code in [401, 422]  # Should require authentication or have validation error
    
    # Test PUT /receipts/{receipt_id}/approve without authentication
    response = client_no_db.put("/api/v1/receipts/test-receipt-id/approve")
    assert response.status_code in [401, 422]  # Should require authentication or have validation error
    
    # Test PUT /receipts/{receipt_id}/reject without authentication
    response = client_no_db.put("/api/v1/receipts/test-receipt-id/reject")
    assert response.status_code in [401, 422]  # Should require authentication or have validation error


def test_receipt_upload_requires_authentication(client_no_db: TestClient):
    """Test that receipt upload requires authentication."""
    # Test with empty data
    response = client_no_db.post("/api/v1/receipts/upload")
    assert response.status_code in [401, 422]


def test_receipt_approval_requires_authentication(client_no_db: TestClient):
    """Test that receipt approval requires authentication."""
    response = client_no_db.put("/api/v1/receipts/test-receipt-id/approve")
    assert response.status_code in [401, 422]


def test_receipt_rejection_requires_authentication(client_no_db: TestClient):
    """Test that receipt rejection requires authentication."""
    response = client_no_db.put("/api/v1/receipts/test-receipt-id/reject")
    assert response.status_code in [401, 422] 