from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import require_treasurer_role
from app.core.db import get_session
from app.models.models import User, Receipt, ReceiptStatus, ReceiptTaxBreakdown

router = APIRouter()

@router.post("/generate-refund-package")
async def generate_refund_package(
    start_date: date,
    end_date: date,
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Generate E-585 and E-536R forms for a given period (Treasurer only).
    """
    # Get approved receipts for the period
    receipts = session.exec(
        select(Receipt).where(
            Receipt.organization_id == str(current_user.organization_id),
            Receipt.status == ReceiptStatus.approved,
            Receipt.purchase_date >= start_date,
            Receipt.purchase_date <= end_date
        )
    ).all()
    
    if not receipts:
        raise HTTPException(status_code=404, detail="No approved receipts found for the specified period")
    
    # Aggregate data for E-585
    total_amount = sum(receipt.total_amount for receipt in receipts)
    total_tax_amount = sum(receipt.tax_amount for receipt in receipts if receipt.tax_amount)
    
    # Check if E-536R is needed (multiple counties)
    counties = set(receipt.county for receipt in receipts if receipt.county)
    needs_e536r = len(counties) > 1
    
    # TODO: Implement actual PDF generation
    # For now, return placeholder URLs
    e585_form_url = f"/api/v1/forms/e585/{start_date}/{end_date}"
    e536r_form_url = f"/api/v1/forms/e536r/{start_date}/{end_date}" if needs_e536r else None
    
    return {
        "e585_form_url": e585_form_url,
        "e536r_form_url": e536r_form_url,
        "summary": {
            "total_receipts": len(receipts),
            "total_amount": total_amount,
            "total_tax_amount": total_tax_amount,
            "counties": list(counties),
            "needs_e536r": needs_e536r
        }
    }

@router.get("/e585/{start_date}/{end_date}")
async def get_e585_form(
    start_date: date,
    end_date: date,
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Get E-585 form PDF for a given period.
    """
    # TODO: Implement actual PDF generation
    # This would use a library like reportlab or weasyprint
    return {"message": "E-585 PDF generation not yet implemented"}

@router.get("/e536r/{start_date}/{end_date}")
async def get_e536r_form(
    start_date: date,
    end_date: date,
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Get E-536R form PDF for a given period.
    """
    # TODO: Implement actual PDF generation
    return {"message": "E-536R PDF generation not yet implemented"} 