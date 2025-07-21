"""
Test scenarios and integration tests for GoodStewards backend.

This file demonstrates how to organize and run comprehensive test scenarios
based on the use cases and technical specifications.
"""

import pytest
import json
from typing import Dict, Any
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.test_data import (
    TestScenarios, ORGANIZATIONS, USERS, RECEIPTS, 
    FEEDBACK, create_test_image_data, create_test_csv_data
)


class TestReceiptSubmissionScenarios:
    """Test scenarios for Use Case 1.1: Receipt Submission and AI Extraction."""
    
    def test_successful_receipt_extraction(self, client: TestClient, auth_headers: Dict[str, str]):
        """Test successful AI extraction of receipt data."""
        scenario = TestScenarios.RECEIPT_SUBMISSION_SCENARIOS["successful_extraction"]
        
        # Use actual receipt image data
        image_data = create_test_image_data("1-receipt.png")
        
        # Submit receipt
        response = client.post(
            "/api/v1/receipts/upload",
            files={"image": ("1-receipt.png", image_data, "image/png")},
            data={"is_donation": "false"},
            headers=auth_headers
        )
        
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == scenario["expected_output"]["status"]
        assert "id" in data
        assert "image_url" in data
    
    def test_failed_receipt_extraction(self, client: TestClient, auth_headers: Dict[str, str]):
        """Test failed AI extraction of receipt data."""
        scenario = TestScenarios.RECEIPT_SUBMISSION_SCENARIOS["failed_extraction"]
        
        # Create invalid image data
        invalid_data = b"not_an_image"
        
        response = client.post(
            "/api/v1/receipts/upload",
            files={"image": ("invalid.jpg", invalid_data, "image/jpeg")},
            data={"is_donation": "false"},
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data["detail"]
    
    def test_non_refundable_category(self, client: TestClient, auth_headers: Dict[str, str]):
        """Test receipt with non-refundable category."""
        scenario = TestScenarios.RECEIPT_SUBMISSION_SCENARIOS["non_refundable_category"]
        
        image_data = create_test_image_data("1-receipt.png")
        
        response = client.post(
            "/api/v1/receipts/upload",
            files={"image": ("1-receipt.png", image_data, "image/png")},
            data={"is_donation": "false"},
            headers=auth_headers
        )
        
        # Should be rejected due to non-refundable category
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == "rejected"


class TestSpecialUserScenarios:
    """Test scenarios for Use Case 2.5: Special User Management."""
    
    def test_create_anonymous_donor(self, client: TestClient, treasurer_headers: Dict[str, str]):
        """Test creating anonymous donor profile."""
        scenario = TestScenarios.SPECIAL_USER_SCENARIOS["create_anonymous_donor"]
        
        response = client.post(
            "/api/v1/users/special",
            params={"type": "anonymous_donor"},
            headers=treasurer_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["full_name"] == scenario["expected_output"]["full_name"]
        assert data["is_special_user"] == scenario["expected_output"]["is_special_user"]
        assert data["special_user_type"] == scenario["expected_output"]["special_user_type"]
    
    def test_create_one_time_donor(self, client: TestClient, treasurer_headers: Dict[str, str]):
        """Test creating one-time donor profile."""
        scenario = TestScenarios.SPECIAL_USER_SCENARIOS["create_one_time_donor"]
        
        response = client.post(
            "/api/v1/users/special",
            params={
                "type": "one_time_donor",
                "name": scenario["input"]["name"]
            },
            headers=treasurer_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["full_name"] == scenario["expected_output"]["full_name"]
        assert data["is_special_user"] == scenario["expected_output"]["is_special_user"]


class TestTreasurerSubmissionScenarios:
    """Test scenarios for Use Case 2.6: Treasurer Submits on Behalf."""
    
    def test_submit_for_member(self, client: TestClient, treasurer_headers: Dict[str, str]):
        """Test treasurer submitting receipt on behalf of member."""
        scenario = TestScenarios.TREASURER_SUBMISSION_SCENARIOS["submit_for_member"]
        
        image_data = create_test_image_data("1-receipt.png")
        
        response = client.post(
            "/api/v1/receipts/upload",
            files={"image": ("1-receipt.png", image_data, "image/png")},
            data={
                "is_donation": scenario["input"]["is_donation"],
                "member_id": scenario["input"]["member_id"]
            },
            headers=treasurer_headers
        )
        
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == scenario["expected_output"]["status"]
    
    def test_submit_for_special_user(self, client: TestClient, treasurer_headers: Dict[str, str]):
        """Test treasurer submitting receipt for anonymous donor."""
        scenario = TestScenarios.TREASURER_SUBMISSION_SCENARIOS["submit_for_special_user"]
        
        image_data = create_test_image_data("1-receipt.png")
        
        response = client.post(
            "/api/v1/receipts/upload",
            files={"image": ("1-receipt.png", image_data, "image/png")},
            data={
                "is_donation": scenario["input"]["is_donation"],
                "member_id": scenario["input"]["member_id"]
            },
            headers=treasurer_headers
        )
        
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == scenario["expected_output"]["status"]


class TestFeedbackScenarios:
    """Test scenarios for Use Case 3.1: Feedback Submission."""
    
    def test_submit_bug_report(self, client: TestClient, auth_headers: Dict[str, str]):
        """Test user submitting bug report."""
        scenario = TestScenarios.FEEDBACK_SCENARIOS["submit_bug_report"]
        
        response = client.post(
            "/api/v1/feedback",
            json={
                "category": scenario["input"]["category"],
                "description": scenario["input"]["description"],
                "device_info": scenario["input"]["device_info"]
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["category"] == scenario["expected_output"]["category"]
        assert data["status"] == scenario["expected_output"]["status"]
    
    def test_treasurer_view_feedback(self, client: TestClient, treasurer_headers: Dict[str, str]):
        """Test treasurer viewing organization feedback."""
        scenario = TestScenarios.FEEDBACK_SCENARIOS["treasurer_view_feedback"]
        
        response = client.get(
            "/api/v1/feedback",
            params=scenario["input"],
            headers=treasurer_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= scenario["expected_output"]["count"]


class TestFormGenerationScenarios:
    """Test scenarios for Use Case 1.2: Form Generation."""
    
    def test_generate_e585_single_county(self, client: TestClient, treasurer_headers: Dict[str, str]):
        """Test generating E-585 form for single county."""
        scenario = TestScenarios.FORM_GENERATION_SCENARIOS["generate_e585_single_county"]
        
        response = client.post(
            "/api/v1/forms/generate-refund-package",
            json=scenario["input"],
            headers=treasurer_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "e585_form_url" in data
        assert data.get("e536r_form_url") is None
    
    def test_generate_e585_multiple_counties(self, client: TestClient, treasurer_headers: Dict[str, str]):
        """Test generating E-585 and E-536R forms for multiple counties."""
        scenario = TestScenarios.FORM_GENERATION_SCENARIOS["generate_e585_multiple_counties"]
        
        response = client.post(
            "/api/v1/forms/generate-refund-package",
            json=scenario["input"],
            headers=treasurer_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "e585_form_url" in data
        assert "e536r_form_url" in data


class TestIntegrationScenarios:
    """Integration test scenarios that test multiple use cases together."""
    
    def test_complete_receipt_workflow(self, client: TestClient, treasurer_headers: Dict[str, str]):
        """Test complete receipt workflow: upload -> approve -> payment reconciliation."""
        
        # 1. Upload receipt using actual image
        image_data = create_test_image_data("1-receipt.png")
        upload_response = client.post(
            "/api/v1/receipts/upload",
            files={"image": ("1-receipt.png", image_data, "image/png")},
            data={"is_donation": "false"},
            headers=treasurer_headers
        )
        assert upload_response.status_code == 202
        receipt_id = upload_response.json()["id"]
        
        # 2. Approve receipt
        approve_response = client.put(
            f"/api/v1/receipts/{receipt_id}/approve",
            json={
                "payment_method": "zelle",
                "payment_reference": "ZELLE12345",
                "payment_proof_url": "https://example.com/proof.jpg"
            },
            headers=treasurer_headers
        )
        assert approve_response.status_code == 200
        
        # 3. Upload payment CSV
        csv_data = create_test_csv_data()
        csv_response = client.post(
            "/api/v1/payments/upload-csv",
            files={"csv_file": ("payments.csv", csv_data, "text/csv")},
            headers=treasurer_headers
        )
        assert csv_response.status_code == 200
    
    def test_special_user_donation_workflow(self, client: TestClient, treasurer_headers: Dict[str, str]):
        """Test workflow for anonymous donor submission."""
        
        # 1. Create anonymous donor
        donor_response = client.post(
            "/api/v1/users/special",
            params={"type": "anonymous_donor"},
            headers=treasurer_headers
        )
        assert donor_response.status_code == 201
        donor_id = donor_response.json()["id"]
        
        # 2. Submit donation receipt for anonymous donor using actual image
        image_data = create_test_image_data("1-receipt.png")
        receipt_response = client.post(
            "/api/v1/receipts/upload",
            files={"image": ("1-receipt.png", image_data, "image/png")},
            data={
                "is_donation": "true",
                "member_id": donor_id
            },
            headers=treasurer_headers
        )
        assert receipt_response.status_code == 202
        
        # 3. Verify receipt is marked as donation
        receipt_id = receipt_response.json()["id"]
        get_response = client.get(
            f"/api/v1/receipts/{receipt_id}",
            headers=treasurer_headers
        )
        assert get_response.status_code == 200
        receipt_data = get_response.json()
        assert receipt_data["is_donation"] is True


# =============================================================================
# FIXTURES FOR TEST SCENARIOS
# =============================================================================

@pytest.fixture
def auth_headers(client: TestClient) -> Dict[str, str]:
    """Create authentication headers for regular user."""
    # This would normally involve logging in and getting a token
    # For testing, we'll use a mock token
    return {"Authorization": "Bearer test_token_member"}

@pytest.fixture
def treasurer_headers(client: TestClient) -> Dict[str, str]:
    """Create authentication headers for treasurer user."""
    # This would normally involve logging in and getting a token
    # For testing, we'll use a mock token
    return {"Authorization": "Bearer test_token_treasurer"}

@pytest.fixture
def populated_database(session: Session):
    """Populate database with test data for integration tests."""
    # This fixture would create all the test data in the database
    # Implementation would depend on your database setup
    pass 