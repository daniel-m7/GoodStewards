import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime
from database import create_tables
from baml_client import baml as baml_client
from baml_client.baml_types import Image
import base64

load_dotenv()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()


class Organization(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    fein: str
    ntee_code: str
    address: str
    city: str
    state: str
    zip_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    organization_id: UUID
    full_name: str
    email: str
    role: str  # 'member' or 'treasurer'
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Receipt(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID
    organization_id: UUID
    image_url: str
    vendor_name: Optional[str] = None
    purchase_date: Optional[str] = None
    county: Optional[str] = None
    subtotal_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    expense_category: Optional[str] = None
    status: str  # 'processing', 'pending', 'approved', 'rejected', 'paid'
    is_donation: bool = False
    payment_method: Optional[str] = None  # 'zelle', 'check', 'other'
    payment_reference: Optional[str] = None
    payment_proof_url: Optional[str] = None
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = None

class PaymentTransaction(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    organization_id: UUID
    transaction_date: date
    amount: float
    reference_id: Optional[str] = None
    receipt_id: Optional[UUID] = None

class ReceiptTaxBreakdown(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    receipt_id: UUID
    tax_type: str  # 'state', 'county', 'transit', 'food'
    amount: float

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/users/me", response_model=User)
def get_current_user():
    # Placeholder for OAuth2 logic
    return {
        "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
        "organization_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "role": "member"
    }

@app.get("/api/organizations/{organization_id}", response_model=Organization)
def get_organization(organization_id: UUID):
    # Placeholder for database logic
    return {
        "id": organization_id,
        "name": "Nonprofit Org",
        "fein": "12-3456789",
        "ntee_code": "A01",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "NC",
        "zip_code": "12345"
    }

from baml_client import baml as baml_client
from baml_client.baml_types import Image
import base64

# BAML client instance
baml = baml_client.BAMLClient()

# BAML client instance
baml = baml_client.BAMLClient()

@app.post("/api/receipts/upload", status_code=202)
async def upload_receipt(image: bytes, is_donation: bool = False, member_id: Optional[UUID] = None):
    # Use BAML to extract data from the image
    img = Image(base64=base64.b64encode(image).decode("utf-8"))
    extracted_data = await baml.ExtractReceiptData(receipt=img)

    # Placeholder for saving to database and R2
    # In a real implementation, you would map extracted_data to your Receipt model
    # and save it to the database.
    print(extracted_data)

    return {"id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13", "status": "processing", "image_url": "url-to-uploaded-image"}

@app.get("/api/receipts", response_model=List[Receipt])
def get_receipts(status: Optional[str] = None, user_id: Optional[UUID] = None, limit: int = 10, offset: int = 0):
    # Placeholder for database logic
    return [
        {
            "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13",
            "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            "organization_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12",
            "image_url": "url-to-image",
            "vendor_name": "Grocery Store",
            "purchase_date": "2023-01-15",
            "total_amount": 55.75,
            "status": "pending"
        }
    ]

@app.get("/api/receipts/{receipt_id}", response_model=Receipt)
def get_receipt(receipt_id: UUID):
    # Placeholder for database logic
    return {
        "id": receipt_id,
        "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
        "organization_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12",
        "image_url": "url-to-image",
        "vendor_name": "Grocery Store",
        "purchase_date": "2023-01-15",
        "county": "Wake",
        "subtotal_amount": 50.00,
        "tax_amount": 5.75,
        "total_amount": 55.75,
        "expense_category": "Food",
        "status": "pending",
        "is_donation": False,
        "submitted_at": "2023-01-15T10:00:00Z",
        "tax_breakdowns": [
            {"tax_type": "state", "amount": 3.00},
            {"tax_type": "county", "amount": 2.75}
        ]
    }

@app.put("/api/receipts/{receipt_id}/approve", response_model=Receipt)
def approve_receipt(receipt_id: UUID, payment_method: str, payment_reference: str, payment_proof_url: str):
    # Placeholder for database logic
    return {
        "id": receipt_id,
        "status": "approved",
        "approved_at": "2023-01-16T11:00:00Z"
    }

@app.put("/api/receipts/{receipt_id}/reject", response_model=Receipt)
def reject_receipt(receipt_id: UUID, reason: str):
    # Placeholder for database logic
    return {
        "id": receipt_id,
        "status": "rejected"
    }

@app.post("/api/forms/generate-refund-package")
def generate_refund_package(start_date: date, end_date: date):
    # Placeholder for PDF generation logic
    return {
        "e585_form_url": "url-to-generated-e585-pdf",
        "e536r_form_url": "url-to-generated-e536r-pdf"
    }

@app.post("/api/payments/upload-csv")
def upload_csv(csv_file: bytes):
    # Placeholder for CSV processing logic
    return {
        "message": "CSV uploaded and processing",
        "processed_records": 100,
        "matched_receipts": 80,
        "unmatched_records": 20
    }

@app.post("/api/payments/match-manual")
def match_manual(transaction_id: UUID, receipt_id: UUID):
    # Placeholder for database logic
    return {"message": "Payment matched successfully"}


