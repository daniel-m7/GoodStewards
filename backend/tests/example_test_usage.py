"""
Example usage of test data and scenarios.

This file demonstrates how to use the test data and scenarios in your actual tests.
It shows best practices for organizing test cases and using the test data effectively.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.test_data import (
    ORGANIZATIONS, USERS, RECEIPTS, FEEDBACK,
    TestScenarios, create_test_image_data
)


# =============================================================================
# EXAMPLE 1: Simple Test Using Test Data
# =============================================================================

def test_user_creation_with_test_data(client: TestClient):
    """Example: Using predefined test data for user creation."""
    
    # Use test data from test_data.py
    user_data = USERS["member_1"]
    
    response = client.post(
        "/api/v1/users/",
        json={
            "full_name": user_data["full_name"],
            "email": user_data["email"],
            "password": "testpassword123",
            "role": user_data["role"]
        }
    )
    
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["full_name"] == user_data["full_name"]
    assert created_user["email"] == user_data["email"]


# =============================================================================
# EXAMPLE 2: Test Using Scenarios
# =============================================================================

def test_receipt_upload_scenario(client: TestClient, auth_headers: dict):
    """Example: Using test scenarios for receipt upload."""
    
    # Get the scenario from TestScenarios
    scenario = TestScenarios.RECEIPT_SUBMISSION_SCENARIOS["successful_extraction"]
    
    # Use actual receipt image data
    image_data = create_test_image_data("1-receipt.png")
    
    response = client.post(
        "/api/v1/receipts/upload",
        files={"image": ("1-receipt.png", image_data, "image/png")},
        data={"is_donation": "false"},
        headers=auth_headers
    )
    
    # Verify against expected output
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == scenario["expected_output"]["status"]


# =============================================================================
# EXAMPLE 3: Parameterized Tests with Test Data
# =============================================================================

@pytest.mark.parametrize("user_key", ["member_1", "member_2", "treasurer"])
def test_user_roles_with_test_data(client: TestClient, user_key: str):
    """Example: Parameterized test using different test users."""
    
    user_data = USERS[user_key]
    
    response = client.post(
        "/api/v1/users/",
        json={
            "full_name": user_data["full_name"],
            "email": f"test_{user_key}@example.com",
            "password": "testpassword123",
            "role": user_data["role"]
        }
    )
    
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["role"] == user_data["role"]


# =============================================================================
# EXAMPLE 4: Integration Test with Multiple Test Data
# =============================================================================

def test_organization_with_users_workflow(client: TestClient):
    """Example: Integration test using multiple test data sets."""
    
    # 1. Create organization
    org_data = ORGANIZATIONS["test_org"]
    org_response = client.post(
        "/api/v1/organizations/",
        json=org_data
    )
    assert org_response.status_code == 201
    org_id = org_response.json()["id"]
    
    # 2. Create users for the organization
    for user_key in ["treasurer", "member_1", "member_2"]:
        user_data = USERS[user_key].copy()
        user_data["organization_id"] = org_id
        
        user_response = client.post(
            "/api/v1/users/",
            json=user_data
        )
        assert user_response.status_code == 201
    
    # 3. Verify organization has users
    org_users_response = client.get(f"/api/v1/organizations/{org_id}/users")
    assert org_users_response.status_code == 200
    users = org_users_response.json()
    assert len(users) == 3


# =============================================================================
# EXAMPLE 5: Test with Custom Test Data
# =============================================================================

def test_custom_receipt_scenario(client: TestClient, auth_headers: dict):
    """Example: Creating custom test data for specific scenarios."""
    
    # Custom test data for this specific test
    custom_receipt = {
        "vendor_name": "Custom Store",
        "purchase_date": "2023-12-01",
        "county": "Wake",
        "subtotal_amount": 100.00,
        "tax_amount": 11.00,
        "total_amount": 111.00,
        "expense_category": "Office Supplies",
        "is_donation": False
    }
    
    # Use actual receipt image
    image_data = create_test_image_data("1-receipt.png")
    
    response = client.post(
        "/api/v1/receipts/upload",
        files={"image": ("1-receipt.png", image_data, "image/png")},
        data={"is_donation": "false"},
        headers=auth_headers
    )
    
    assert response.status_code == 202
    data = response.json()
    assert data["status"] in ["pending", "processing"]


# =============================================================================
# EXAMPLE 6: Test Using Feedback Scenarios
# =============================================================================

def test_feedback_workflow_scenario(client: TestClient, auth_headers: dict, treasurer_headers: dict):
    """Example: Testing feedback workflow using scenarios."""
    
    # 1. Submit feedback (member)
    feedback_scenario = TestScenarios.FEEDBACK_SCENARIOS["submit_bug_report"]
    
    submit_response = client.post(
        "/api/v1/feedback",
        json=feedback_scenario["input"],
        headers=auth_headers
    )
    assert submit_response.status_code == 201
    
    # 2. View feedback (treasurer)
    view_scenario = TestScenarios.FEEDBACK_SCENARIOS["treasurer_view_feedback"]
    
    view_response = client.get(
        "/api/v1/feedback",
        params=view_scenario["input"],
        headers=treasurer_headers
    )
    assert view_response.status_code == 200
    
    feedback_list = view_response.json()
    assert len(feedback_list) > 0


# =============================================================================
# EXAMPLE 7: Test Data Utilities
# =============================================================================

def test_using_test_data_utilities():
    """Example: Using test data utility functions."""
    
    from tests.test_data import get_test_data_by_type, get_test_scenario, get_available_receipt_images
    
    # Get all user test data
    users_data = get_test_data_by_type("users")
    assert "treasurer" in users_data
    assert "member_1" in users_data
    
    # Get specific scenario
    scenario = get_test_scenario("receipt_submission", "successful_extraction")
    assert scenario["description"] is not None
    assert "input" in scenario
    assert "expected_output" in scenario
    
    # Get available receipt images
    available_images = get_available_receipt_images()
    assert "1-receipt.png" in available_images


# =============================================================================
# EXAMPLE 8: Database State Testing
# =============================================================================

def test_database_state_with_test_data(session: Session):
    """Example: Testing database state using test data."""
    
    # This would typically involve creating test data in the database
    # and then verifying the state
    
    # Example: Verify organization exists
    from app.models.models import Organization
    
    org_data = ORGANIZATIONS["test_org"]
    org = session.get(Organization, org_data["id"])
    
    if org:
        assert org.name == org_data["name"]
        assert org.fein == org_data["fein"]


# =============================================================================
# EXAMPLE 9: Testing with Multiple Receipt Images
# =============================================================================

def test_multiple_receipt_images(client: TestClient, auth_headers: dict):
    """Example: Testing with different receipt images."""
    
    from tests.test_data import get_available_receipt_images
    
    available_images = get_available_receipt_images()
    
    for image_name in available_images[:2]:  # Test first 2 images
        image_data = create_test_image_data(image_name)
        
        response = client.post(
            "/api/v1/receipts/upload",
            files={"image": (image_name, image_data, "image/png")},
            data={"is_donation": "false"},
            headers=auth_headers
        )
        
        assert response.status_code == 202
        data = response.json()
        assert "id" in data
        assert "image_url" in data


# =============================================================================
# BEST PRACTICES SUMMARY
# =============================================================================

"""
BEST PRACTICES FOR TEST DATA AND SCENARIOS:

1. ORGANIZATION:
   - Keep test data in test_data.py
   - Keep scenarios in TestScenarios class
   - Use descriptive names for test data keys
   - Group related data together

2. USAGE:
   - Use test_data.py for predefined data
   - Use TestScenarios for workflow testing
   - Create custom data for specific test cases
   - Use parameterized tests for multiple scenarios

3. MAINTENANCE:
   - Update test data when models change
   - Keep scenarios aligned with use cases
   - Document complex test scenarios
   - Use fixtures for common setup

4. STRUCTURE:
   - test_data.py: All test data and scenarios
   - test_scenarios.py: Integration test examples
   - example_test_usage.py: Usage examples (this file)
   - conftest.py: Pytest fixtures and configuration

5. NAMING CONVENTIONS:
   - Test data keys: descriptive (e.g., "treasurer", "food_receipt")
   - Scenario names: use_case_description (e.g., "successful_extraction")
   - Test functions: test_scenario_name (e.g., test_successful_extraction)

6. DATA TYPES:
   - Use enums from models for status/type fields
   - Use proper date/datetime objects
   - Use UUIDs for IDs
   - Use realistic but test-safe data

7. IMAGE TESTING:
   - Use actual receipt images from data/ directory
   - Use create_test_image_data() function
   - Test with multiple image types
   - Verify image upload and processing
""" 