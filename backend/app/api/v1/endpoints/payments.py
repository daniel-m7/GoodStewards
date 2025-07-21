import csv
import io
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from datetime import date

from app.core.auth import require_treasurer_role
from app.core.db import get_session
from app.models.models import User, PaymentTransaction, Receipt, ReceiptStatus

router = APIRouter()

@router.post("/upload-csv")
async def upload_payment_csv(
    csv_file: UploadFile = File(...),
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Upload CSV of payment transactions for reconciliation (Treasurer only).
    """
    if not csv_file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Read CSV content
    content = await csv_file.read()
    csv_text = content.decode('utf-8')
    
    # Parse CSV
    csv_reader = csv.DictReader(io.StringIO(csv_text))
    
    processed_records = 0
    matched_receipts = 0
    unmatched_records = 0
    
    for row in csv_reader:
        processed_records += 1
        
        # Extract payment data from CSV
        # Expected columns: transaction_date, amount, reference_id
        try:
            transaction_date = date.fromisoformat(row['transaction_date'])
            amount = float(row['amount'])
            reference_id = row.get('reference_id', '')
        except (KeyError, ValueError) as e:
            unmatched_records += 1
            continue
        
        # Try to match with existing receipts
        receipt = session.exec(
            select(Receipt).where(
                Receipt.organization_id == str(current_user.organization_id),
                Receipt.status == ReceiptStatus.approved,
                Receipt.payment_reference == reference_id
            )
        ).first()
        
        if receipt:
            # Create payment transaction and link to receipt
            payment_transaction = PaymentTransaction(
                organization_id=str(current_user.organization_id),
                transaction_date=transaction_date,
                amount=amount,
                reference_id=reference_id,
                receipt_id=str(receipt.id)
            )
            session.add(payment_transaction)
            
            # Update receipt status to paid
            receipt.status = ReceiptStatus.paid
            session.add(receipt)
            
            matched_receipts += 1
        else:
            # Create unmatched payment transaction
            payment_transaction = PaymentTransaction(
                organization_id=str(current_user.organization_id),
                transaction_date=transaction_date,
                amount=amount,
                reference_id=reference_id
            )
            session.add(payment_transaction)
            unmatched_records += 1
    
    session.commit()
    
    return {
        "message": "CSV uploaded and processing",
        "processed_records": processed_records,
        "matched_receipts": matched_receipts,
        "unmatched_records": unmatched_records
    }

@router.post("/match-manual")
async def match_payment_manual(
    transaction_id: str,
    receipt_id: str,
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Manually match an unmatched payment transaction to a receipt (Treasurer only).
    """
    # Find the payment transaction
    transaction = session.exec(
        select(PaymentTransaction).where(
            PaymentTransaction.id == transaction_id,
            PaymentTransaction.organization_id == str(current_user.organization_id),
            PaymentTransaction.receipt_id.is_(None)  # Unmatched
        )
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Unmatched payment transaction not found")
    
    # Find the receipt
    receipt = session.exec(
        select(Receipt).where(
            Receipt.id == receipt_id,
            Receipt.organization_id == str(current_user.organization_id),
            Receipt.status == ReceiptStatus.approved
        )
    ).first()
    
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    # Link transaction to receipt
    transaction.receipt_id = receipt_id
    session.add(transaction)
    
    # Update receipt status to paid
    receipt.status = ReceiptStatus.paid
    session.add(receipt)
    
    session.commit()
    
    return {
        "message": "Payment matched successfully",
        "transaction_id": str(transaction.id),
        "receipt_id": str(receipt.id)
    }

@router.get("/unmatched")
async def get_unmatched_payments(
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Get unmatched payment transactions (Treasurer only).
    """
    transactions = session.exec(
        select(PaymentTransaction).where(
            PaymentTransaction.organization_id == str(current_user.organization_id),
            PaymentTransaction.receipt_id.is_(None)
        )
    ).all()
    
    return [
        {
            "id": str(transaction.id),
            "transaction_date": transaction.transaction_date.isoformat(),
            "amount": transaction.amount,
            "reference_id": transaction.reference_id
        }
        for transaction in transactions
    ]

@router.get("/unpaid-receipts")
async def get_unpaid_receipts(
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Get approved receipts that haven't been paid (Treasurer only).
    """
    receipts = session.exec(
        select(Receipt).where(
            Receipt.organization_id == str(current_user.organization_id),
            Receipt.status == ReceiptStatus.approved
        )
    ).all()
    
    return [
        {
            "id": str(receipt.id),
            "user_id": str(receipt.user_id),
            "vendor_name": receipt.vendor_name,
            "total_amount": receipt.total_amount,
            "payment_reference": receipt.payment_reference,
            "approved_at": receipt.approved_at.isoformat() if receipt.approved_at else None
        }
        for receipt in receipts
    ] 