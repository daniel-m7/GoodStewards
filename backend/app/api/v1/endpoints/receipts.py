import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlmodel import Session, select
from datetime import date, datetime

from app.core.auth import get_current_active_user, require_treasurer_role
from app.core.db import get_session
from app.models.models import User, Receipt, ReceiptStatus, ReceiptTaxBreakdown, TaxType
from app.services.baml_service import BAMLService
from app.services.storage_service import R2StorageService

router = APIRouter()

# Load non-refundable categories
def load_nonrefundable_categories():
    try:
        with open("config/nonrefundable_categories.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@router.post("/upload")
async def upload_receipt(
    image: UploadFile = File(...),
    is_donation: bool = Form(False),
    member_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Upload a receipt image for AI-powered data extraction.
    """
    # Validate file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read image data
    image_data = await image.read()
    
    # Upload to R2 storage
    storage_service = R2StorageService()
    image_url = await storage_service.upload_image(image_data, image.content_type)
    
    if not image_url:
        raise HTTPException(status_code=500, detail="Failed to upload image")
    
    # Extract data using BAML
    baml_service = BAMLService()
    extracted_data = await baml_service.extract_receipt_data(image_data, image.content_type)
    
    # Determine user for the receipt
    receipt_user_id = member_id if member_id and current_user.role == "treasurer" else str(current_user.id)
    
    # Check if user exists and belongs to same organization
    if member_id and current_user.role == "treasurer":
        statement = select(User).where(
            User.id == member_id,
            User.organization_id == current_user.organization_id
        )
        member = session.exec(statement).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
    
    # Create receipt record
    receipt = Receipt(
        image_url=image_url,
        user_id=receipt_user_id,
        organization_id=str(current_user.organization_id),
        is_donation=is_donation,
        status=ReceiptStatus.processing
    )
    
    # If AI extraction was successful, populate fields
    if extracted_data and baml_service.validate_extracted_data(extracted_data):
        # Check if category is refundable
        nonrefundable_categories = load_nonrefundable_categories()
        if extracted_data.expense_category in nonrefundable_categories:
            receipt.status = ReceiptStatus.rejected
        else:
            receipt.status = ReceiptStatus.pending
            receipt.vendor_name = extracted_data.vendor_name
            receipt.purchase_date = extracted_data.purchase_date
            receipt.county = extracted_data.county
            receipt.subtotal_amount = extracted_data.subtotal_amount
            receipt.tax_amount = extracted_data.tax_amount
            receipt.total_amount = extracted_data.total_amount
            receipt.expense_category = extracted_data.expense_category
            
            # Add tax breakdowns
            if extracted_data.tax_breakdowns:
                for breakdown in extracted_data.tax_breakdowns:
                    tax_breakdown = ReceiptTaxBreakdown(
                        tax_type=TaxType(breakdown.tax_type.value),
                        amount=breakdown.amount,
                        receipt_id=str(receipt.id)
                    )
                    session.add(tax_breakdown)
    
    session.add(receipt)
    session.commit()
    session.refresh(receipt)
    
    return {
        "id": str(receipt.id),
        "status": receipt.status,
        "image_url": receipt.image_url,
        "message": "Receipt uploaded successfully"
    }

@router.get("/")
async def get_receipts(
    status: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    is_donation: Optional[bool] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get receipts with filtering and pagination.
    """
    # Build query
    query = select(Receipt).where(Receipt.organization_id == str(current_user.organization_id))
    
    # Apply filters
    if status:
        query = query.where(Receipt.status == status)
    
    if is_donation is not None:
        query = query.where(Receipt.is_donation == is_donation)
    
    if user_id:
        # Only treasurers can filter by user_id
        if current_user.role != "treasurer":
            raise HTTPException(status_code=403, detail="Treasurer role required")
        query = query.where(Receipt.user_id == user_id)
    else:
        # Members can only see their own receipts
        if current_user.role == "member":
            query = query.where(Receipt.user_id == str(current_user.id))
    
    # Apply pagination
    query = query.offset(offset).limit(limit)
    
    receipts = session.exec(query).all()
    
    return [
        {
            "id": str(receipt.id),
            "user_id": str(receipt.user_id),
            "vendor_name": receipt.vendor_name,
            "purchase_date": receipt.purchase_date.isoformat() if receipt.purchase_date else None,
            "total_amount": receipt.total_amount,
            "status": receipt.status,
            "is_donation": receipt.is_donation,
            "submitted_at": receipt.submitted_at.isoformat()
        }
        for receipt in receipts
    ]

@router.get("/{receipt_id}")
async def get_receipt(
    receipt_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get detailed receipt information.
    """
    # Build query with access control
    query = select(Receipt).where(
        Receipt.id == receipt_id,
        Receipt.organization_id == str(current_user.organization_id)
    )
    
    # Members can only see their own receipts
    if current_user.role == "member":
        query = query.where(Receipt.user_id == str(current_user.id))
    
    receipt = session.exec(query).first()
    
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    # Get tax breakdowns
    tax_breakdowns = session.exec(
        select(ReceiptTaxBreakdown).where(ReceiptTaxBreakdown.receipt_id == receipt_id)
    ).all()
    
    return {
        "id": str(receipt.id),
        "user_id": str(receipt.user_id),
        "organization_id": str(receipt.organization_id),
        "image_url": receipt.image_url,
        "vendor_name": receipt.vendor_name,
        "purchase_date": receipt.purchase_date.isoformat() if receipt.purchase_date else None,
        "county": receipt.county,
        "subtotal_amount": receipt.subtotal_amount,
        "tax_amount": receipt.tax_amount,
        "total_amount": receipt.total_amount,
        "expense_category": receipt.expense_category,
        "status": receipt.status,
        "is_donation": receipt.is_donation,
        "payment_method": receipt.payment_method,
        "payment_reference": receipt.payment_reference,
        "payment_proof_url": receipt.payment_proof_url,
        "submitted_at": receipt.submitted_at.isoformat(),
        "approved_at": receipt.approved_at.isoformat() if receipt.approved_at else None,
        "tax_breakdowns": [
            {
                "tax_type": breakdown.tax_type,
                "amount": breakdown.amount
            }
            for breakdown in tax_breakdowns
        ]
    }

@router.put("/{receipt_id}/approve")
async def approve_receipt(
    receipt_id: str,
    payment_method: str,
    payment_reference: str,
    payment_proof_url: Optional[str] = None,
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Approve a receipt (Treasurer only).
    """
    # Find receipt
    receipt = session.exec(
        select(Receipt).where(
            Receipt.id == receipt_id,
            Receipt.organization_id == str(current_user.organization_id)
        )
    ).first()
    
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    if receipt.status != ReceiptStatus.pending:
        raise HTTPException(status_code=400, detail="Receipt is not pending")
    
    # Update receipt
    receipt.status = ReceiptStatus.approved
    receipt.payment_method = payment_method
    receipt.payment_reference = payment_reference
    receipt.payment_proof_url = payment_proof_url
    receipt.approved_at = datetime.utcnow()
    
    session.add(receipt)
    session.commit()
    session.refresh(receipt)
    
    return {
        "id": str(receipt.id),
        "status": receipt.status,
        "approved_at": receipt.approved_at.isoformat()
    }

@router.put("/{receipt_id}/reject")
async def reject_receipt(
    receipt_id: str,
    reason: str,
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Reject a receipt (Treasurer only).
    """
    # Find receipt
    receipt = session.exec(
        select(Receipt).where(
            Receipt.id == receipt_id,
            Receipt.organization_id == str(current_user.organization_id)
        )
    ).first()
    
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    if receipt.status != ReceiptStatus.pending:
        raise HTTPException(status_code=400, detail="Receipt is not pending")
    
    # Update receipt
    receipt.status = ReceiptStatus.rejected
    
    session.add(receipt)
    session.commit()
    session.refresh(receipt)
    
    return {
        "id": str(receipt.id),
        "status": receipt.status,
        "rejection_reason": reason
    } 