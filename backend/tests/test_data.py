"""
Test data and scenarios for GoodStewards backend tests.

This file contains all the test data, scenarios, and fixtures needed for comprehensive testing
of the GoodStewards application. It follows the project's use cases and technical specifications.
"""

import uuid
from datetime import date, datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path
from app.models.models import Role, SpecialUserType, ReceiptStatus, PaymentMethod, TaxType, FeedbackCategory, FeedbackStatus


# =============================================================================
# ORGANIZATION TEST DATA
# =============================================================================

ORGANIZATIONS = {
    "test_org": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Test Nonprofit Organization",
        "fein": "12-3456789",
        "ntee_code": "A01",
        "address": "123 Test Street",
        "city": "Raleigh",
        "state": "NC",
        "zip_code": "27601"
    },
    "church_org": {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "name": "First Baptist Church",
        "fein": "98-7654321",
        "ntee_code": "X20",
        "address": "456 Church Avenue",
        "city": "Durham",
        "state": "NC",
        "zip_code": "27701"
    },
    "charity_org": {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "name": "Local Food Bank",
        "fein": "55-1234567",
        "ntee_code": "K31",
        "address": "789 Charity Lane",
        "city": "Chapel Hill",
        "state": "NC",
        "zip_code": "27514"
    }
}


# =============================================================================
# USER TEST DATA
# =============================================================================

USERS = {
    "treasurer": {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "full_name": "John Treasurer",
        "email": "treasurer@testorg.com",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2",  # "password123"
        "role": Role.treasurer,
        "contact_telephone": "+1-555-123-4567",
        "is_special_user": False,
        "special_user_type": None,
        "organization_id": ORGANIZATIONS["test_org"]["id"]
    },
    "member_1": {
        "id": "660e8400-e29b-41d4-a716-446655440002",
        "full_name": "Alice Member",
        "email": "alice@testorg.com",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2",
        "role": Role.member,
        "contact_telephone": "+1-555-234-5678",
        "is_special_user": False,
        "special_user_type": None,
        "organization_id": ORGANIZATIONS["test_org"]["id"]
    },
    "member_2": {
        "id": "660e8400-e29b-41d4-a716-446655440003",
        "full_name": "Bob Volunteer",
        "email": "bob@testorg.com",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2",
        "role": Role.member,
        "contact_telephone": "+1-555-345-6789",
        "is_special_user": False,
        "special_user_type": None,
        "organization_id": ORGANIZATIONS["test_org"]["id"]
    },
    "anonymous_donor": {
        "id": "660e8400-e29b-41d4-a716-446655440004",
        "full_name": "Anonymous Donor",
        "email": None,
        "hashed_password": None,
        "role": Role.member,
        "contact_telephone": None,
        "is_special_user": True,
        "special_user_type": SpecialUserType.anonymous_donor,
        "organization_id": ORGANIZATIONS["test_org"]["id"]
    },
    "unknown_user": {
        "id": "660e8400-e29b-41d4-a716-446655440005",
        "full_name": "Unknown User",
        "email": None,
        "hashed_password": None,
        "role": Role.member,
        "contact_telephone": None,
        "is_special_user": True,
        "special_user_type": SpecialUserType.unknown_user,
        "organization_id": ORGANIZATIONS["test_org"]["id"]
    },
    "one_time_donor": {
        "id": "660e8400-e29b-41d4-a716-446655440006",
        "full_name": "Jane Smith",
        "email": None,
        "hashed_password": None,
        "role": Role.member,
        "contact_telephone": None,
        "is_special_user": True,
        "special_user_type": SpecialUserType.one_time_donor,
        "organization_id": ORGANIZATIONS["test_org"]["id"]
    }
}


# =============================================================================
# RECEIPT TEST DATA
# =============================================================================

RECEIPTS = {
    "food_receipt": {
        "id": "770e8400-e29b-41d4-a716-446655440001",
        "user_id": USERS["member_1"]["id"],
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "image_url": "https://r2.example.com/receipts/food_receipt.jpg",
        "vendor_name": "Harris Teeter",
        "purchase_date": date(2023, 1, 15),
        "county": "Wake",
        "subtotal_amount": 50.00,
        "tax_amount": 5.75,
        "total_amount": 55.75,
        "expense_category": "Food",
        "status": ReceiptStatus.pending,
        "is_donation": False,
        "payment_method": None,
        "payment_reference": None,
        "payment_proof_url": None,
        "submitted_at": datetime(2023, 1, 15, 10, 0, 0),
        "approved_at": None
    },
    "office_supplies": {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "user_id": USERS["member_2"]["id"],
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "image_url": "https://r2.example.com/receipts/office_supplies.jpg",
        "vendor_name": "Office Depot",
        "purchase_date": date(2023, 1, 20),
        "county": "Wake",
        "subtotal_amount": 120.00,
        "tax_amount": 12.00,
        "total_amount": 132.00,
        "expense_category": "Office Supplies",
        "status": ReceiptStatus.approved,
        "is_donation": False,
        "payment_method": PaymentMethod.zelle,
        "payment_reference": "ZELLE12345",
        "payment_proof_url": "https://r2.example.com/payments/zelle_proof.jpg",
        "submitted_at": datetime(2023, 1, 20, 14, 30, 0),
        "approved_at": datetime(2023, 1, 21, 9, 0, 0)
    },
    "donation_receipt": {
        "id": "770e8400-e29b-41d4-a716-446655440003",
        "user_id": USERS["anonymous_donor"]["id"],
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "image_url": "https://r2.example.com/receipts/donation.jpg",
        "vendor_name": "Target",
        "purchase_date": date(2023, 1, 25),
        "county": "Durham",
        "subtotal_amount": 200.00,
        "tax_amount": 20.00,
        "total_amount": 220.00,
        "expense_category": "Donations",
        "status": ReceiptStatus.approved,
        "is_donation": True,
        "payment_method": None,
        "payment_reference": None,
        "payment_proof_url": None,
        "submitted_at": datetime(2023, 1, 25, 16, 45, 0),
        "approved_at": datetime(2023, 1, 26, 11, 0, 0)
    },
    "rejected_receipt": {
        "id": "770e8400-e29b-41d4-a716-446655440004",
        "user_id": USERS["member_1"]["id"],
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "image_url": "https://r2.example.com/receipts/rejected.jpg",
        "vendor_name": "Gas Station",
        "purchase_date": date(2023, 1, 30),
        "county": "Wake",
        "subtotal_amount": 45.00,
        "tax_amount": 4.50,
        "total_amount": 49.50,
        "expense_category": "Fuel",
        "status": ReceiptStatus.rejected,
        "is_donation": False,
        "payment_method": None,
        "payment_reference": None,
        "payment_proof_url": None,
        "submitted_at": datetime(2023, 1, 30, 8, 15, 0),
        "approved_at": None
    }
}


# =============================================================================
# TAX BREAKDOWN TEST DATA
# =============================================================================

TAX_BREAKDOWNS = {
    "food_receipt_taxes": [
        {
            "id": "880e8400-e29b-41d4-a716-446655440001",
            "receipt_id": RECEIPTS["food_receipt"]["id"],
            "tax_type": TaxType.state,
            "amount": 3.00
        },
        {
            "id": "880e8400-e29b-41d4-a716-446655440002",
            "receipt_id": RECEIPTS["food_receipt"]["id"],
            "tax_type": TaxType.county,
            "amount": 2.75
        }
    ],
    "office_supplies_taxes": [
        {
            "id": "880e8400-e29b-41d4-a716-446655440003",
            "receipt_id": RECEIPTS["office_supplies"]["id"],
            "tax_type": TaxType.state,
            "amount": 7.20
        },
        {
            "id": "880e8400-e29b-41d4-a716-446655440004",
            "receipt_id": RECEIPTS["office_supplies"]["id"],
            "tax_type": TaxType.county,
            "amount": 4.80
        }
    ]
}


# =============================================================================
# PAYMENT TRANSACTION TEST DATA
# =============================================================================

PAYMENT_TRANSACTIONS = {
    "zelle_payment": {
        "id": "990e8400-e29b-41d4-a716-446655440001",
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "transaction_date": date(2023, 1, 21),
        "amount": 132.00,
        "reference_id": "ZELLE12345",
        "receipt_id": RECEIPTS["office_supplies"]["id"]
    },
    "check_payment": {
        "id": "990e8400-e29b-41d4-a716-446655440002",
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "transaction_date": date(2023, 1, 26),
        "amount": 220.00,
        "reference_id": "CHECK789",
        "receipt_id": RECEIPTS["donation_receipt"]["id"]
    },
    "unmatched_payment": {
        "id": "990e8400-e29b-41d4-a716-446655440003",
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "transaction_date": date(2023, 1, 28),
        "amount": 75.50,
        "reference_id": "ZELLE67890",
        "receipt_id": None
    }
}


# =============================================================================
# FEEDBACK TEST DATA
# =============================================================================

FEEDBACK = {
    "bug_report": {
        "id": "aa0e8400-e29b-41d4-a716-446655440001",
        "user_id": USERS["member_1"]["id"],
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "category": FeedbackCategory.bug_report,
        "description": "App crashes when uploading receipt images",
        "device_info": '{"app_version": "1.0.0", "os": "iOS 16.0", "device_model": "iPhone 14"}',
        "status": FeedbackStatus.submitted,
        "created_at": datetime(2023, 1, 15, 12, 0, 0)
    },
    "feature_request": {
        "id": "aa0e8400-e29b-41d4-a716-446655440002",
        "user_id": USERS["treasurer"]["id"],
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "category": FeedbackCategory.feature_request,
        "description": "Please add bulk receipt upload functionality",
        "device_info": '{"app_version": "1.0.0", "os": "Windows 11", "browser": "Chrome"}',
        "status": FeedbackStatus.in_review,
        "created_at": datetime(2023, 1, 20, 15, 30, 0)
    },
    "testimony": {
        "id": "aa0e8400-e29b-41d4-a716-446655440003",
        "user_id": USERS["member_2"]["id"],
        "organization_id": ORGANIZATIONS["test_org"]["id"],
        "category": FeedbackCategory.testimony,
        "description": "This app has saved us so much time with tax refunds!",
        "device_info": '{"app_version": "1.0.0", "os": "Android 13", "device_model": "Samsung Galaxy S23"}',
        "status": FeedbackStatus.resolved,
        "created_at": datetime(2023, 1, 25, 9, 15, 0)
    }
}


# =============================================================================
# TEST SCENARIOS
# =============================================================================

class TestScenarios:
    """Test scenarios based on use cases from the technical specification."""
    
    # Use Case 1.1: Receipt Submission and AI Extraction
    RECEIPT_SUBMISSION_SCENARIOS = {
        "successful_extraction": {
            "description": "User uploads valid receipt, AI extracts data successfully",
            "input": {
                "image": "1-receipt.png",
                "is_donation": False,
                "member_id": None
            },
            "expected_output": {
                "status": ReceiptStatus.pending,
                "vendor_name": "Walmart",
                "total_amount": 52.20
            }
        },
        "failed_extraction": {
            "description": "User uploads invalid image, AI extraction fails",
            "input": {
                "image": "invalid_image.jpg",
                "is_donation": False,
                "member_id": None
            },
            "expected_output": {
                "status": ReceiptStatus.rejected,
                "error": "Could not extract data from image"
            }
        },
        "non_refundable_category": {
            "description": "User uploads receipt with non-refundable category",
            "input": {
                "image": "1-receipt.png",
                "is_donation": False,
                "member_id": None
            },
            "expected_output": {
                "status": ReceiptStatus.rejected,
                "error": "Non-refundable category"
            }
        }
    }
    
    # Use Case 2.5: Special User Management
    SPECIAL_USER_SCENARIOS = {
        "create_anonymous_donor": {
            "description": "Treasurer creates anonymous donor profile",
            "input": {
                "type": SpecialUserType.anonymous_donor,
                "name": None
            },
            "expected_output": {
                "full_name": "Anonymous Donor",
                "is_special_user": True,
                "special_user_type": SpecialUserType.anonymous_donor
            }
        },
        "create_one_time_donor": {
            "description": "Treasurer creates one-time donor profile",
            "input": {
                "type": SpecialUserType.one_time_donor,
                "name": "Jane Smith"
            },
            "expected_output": {
                "full_name": "Jane Smith",
                "is_special_user": True,
                "special_user_type": SpecialUserType.one_time_donor
            }
        }
    }
    
    # Use Case 2.6: Treasurer Submits on Behalf
    TREASURER_SUBMISSION_SCENARIOS = {
        "submit_for_member": {
            "description": "Treasurer submits receipt on behalf of member",
            "input": {
                "image": "1-receipt.png",
                "is_donation": False,
                "member_id": USERS["member_1"]["id"]
            },
            "expected_output": {
                "user_id": USERS["member_1"]["id"],
                "status": ReceiptStatus.pending
            }
        },
        "submit_for_special_user": {
            "description": "Treasurer submits receipt for anonymous donor",
            "input": {
                "image": "1-receipt.png",
                "is_donation": True,
                "member_id": USERS["anonymous_donor"]["id"]
            },
            "expected_output": {
                "user_id": USERS["anonymous_donor"]["id"],
                "is_donation": True,
                "status": ReceiptStatus.pending
            }
        }
    }
    
    # Use Case 3.1: Feedback Submission
    FEEDBACK_SCENARIOS = {
        "submit_bug_report": {
            "description": "User submits bug report",
            "input": {
                "category": FeedbackCategory.bug_report,
                "description": "App crashes when uploading receipt",
                "device_info": {
                    "app_version": "1.0.0",
                    "os": "iOS 16.0",
                    "device_model": "iPhone 14"
                }
            },
            "expected_output": {
                "category": FeedbackCategory.bug_report,
                "status": FeedbackStatus.submitted
            }
        },
        "treasurer_view_feedback": {
            "description": "Treasurer views organization feedback",
            "input": {
                "category": None,
                "status": None,
                "limit": 10,
                "offset": 0
            },
            "expected_output": {
                "count": 3,
                "items": ["bug_report", "feature_request", "testimony"]
            }
        }
    }
    
    # Use Case 1.2: Form Generation
    FORM_GENERATION_SCENARIOS = {
        "generate_e585_single_county": {
            "description": "Generate E-585 form for single county",
            "input": {
                "start_date": "2023-01-01",
                "end_date": "2023-01-31"
            },
            "expected_output": {
                "e585_form_url": "url-to-e585-pdf",
                "e536r_form_url": None,
                "requires_e536r": False
            }
        },
        "generate_e585_multiple_counties": {
            "description": "Generate E-585 and E-536R forms for multiple counties",
            "input": {
                "start_date": "2023-01-01",
                "end_date": "2023-01-31"
            },
            "expected_output": {
                "e585_form_url": "url-to-e585-pdf",
                "e536r_form_url": "url-to-e536r-pdf",
                "requires_e536r": True
            }
        }
    }


# =============================================================================
# TEST UTILITIES
# =============================================================================

def get_receipt_image_path(image_name: str = "1-receipt.png") -> Path:
    """Get the path to a receipt image file."""
    # Navigate from backend/tests/ to data/ directory
    backend_dir = Path(__file__).parent.parent
    data_dir = backend_dir.parent / "data"
    return data_dir / image_name

def create_test_image_data(image_name: str = "1-receipt.png") -> bytes:
    """Create test image data from actual receipt image files."""
    image_path = get_receipt_image_path(image_name)
    
    if not image_path.exists():
        raise FileNotFoundError(f"Receipt image not found: {image_path}")
    
    with open(image_path, "rb") as f:
        return f.read()

def create_test_csv_data() -> str:
    """Create dummy CSV data for payment reconciliation testing."""
    return """transaction_date,amount,reference_id
2023-01-21,132.00,ZELLE12345
2023-01-26,220.00,CHECK789
2023-01-28,75.50,ZELLE67890"""

def get_test_data_by_type(data_type: str) -> Dict[str, Any]:
    """Get test data by type."""
    data_mapping = {
        "organizations": ORGANIZATIONS,
        "users": USERS,
        "receipts": RECEIPTS,
        "tax_breakdowns": TAX_BREAKDOWNS,
        "payment_transactions": PAYMENT_TRANSACTIONS,
        "feedback": FEEDBACK
    }
    return data_mapping.get(data_type, {})

def get_test_scenario(scenario_type: str, scenario_name: str) -> Dict[str, Any]:
    """Get test scenario by type and name."""
    scenarios = getattr(TestScenarios, f"{scenario_type.upper()}_SCENARIOS", {})
    return scenarios.get(scenario_name, {})

def get_available_receipt_images() -> List[str]:
    """Get list of available receipt image files."""
    data_dir = Path(__file__).parent.parent.parent / "data"
    if data_dir.exists():
        return [f.name for f in data_dir.glob("*.png") if f.is_file()]
    return ["1-receipt.png"]  # Fallback 