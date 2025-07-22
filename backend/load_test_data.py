"""
Load test data into the database for GoodStewards application.

This script populates the database with test data from tests/test_data.py
to create a realistic testing environment.
"""

import asyncio
import uuid
from datetime import datetime, date
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

from tests.test_data import (
    ORGANIZATIONS, USERS, RECEIPTS, TAX_BREAKDOWNS, 
    PAYMENT_TRANSACTIONS, FEEDBACK
)
from app.models.models import (
    Organization, User, Receipt, ReceiptTaxBreakdown, 
    PaymentTransaction, Feedback
)

# Load environment variables
load_dotenv()


def create_test_engine():
    """Create a database engine."""
    # Use the DATABASE_URL from environment or fallback to SQLite
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("⚠️  No DATABASE_URL found, using SQLite for testing")
        database_url = "sqlite:///./test_data.db"
    
    # Convert async URL to sync URL if needed
    if database_url.startswith("postgresql+psycopg_async://"):
        database_url = database_url.replace("postgresql+psycopg_async://", "postgresql://")
    
    # Only replace Docker container name with localhost when running outside Docker
    # Check if we're running inside Docker by looking for the container environment
    if "db:5432" in database_url and not os.path.exists("/.dockerenv"):
        database_url = database_url.replace("db:5432", "localhost:5432")
        print("🔄 Replaced 'db' with 'localhost' for local connection")
    elif "db:5432" in database_url:
        print("🐳 Running inside Docker - using 'db' container name")
    
    print(f"🔗 Connecting to database: {database_url}")
    
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
        poolclass=StaticPool,
    )
    return engine


def load_organizations(session: Session):
    """Load organization test data."""
    print("Loading organizations...")
    
    for org_key, org_data in ORGANIZATIONS.items():
        # Check if organization already exists
        existing_org = session.get(Organization, org_data["id"])
        if existing_org:
            print(f"  Organization {org_key} already exists, skipping...")
            continue
        
        # Create new organization
        org = Organization(
            id=uuid.UUID(org_data["id"]),
            name=org_data["name"],
            fein=org_data["fein"],
            ntee_code=org_data["ntee_code"],
            address=org_data["address"],
            city=org_data["city"],
            state=org_data["state"],
            zip_code=org_data["zip_code"],
            created_at=datetime.now()
        )
        
        session.add(org)
        print(f"  Created organization: {org.name}")
    
    session.commit()
    print(f"  Loaded {len(ORGANIZATIONS)} organizations")


def load_users(session: Session):
    """Load user test data."""
    print("Loading users...")
    
    for user_key, user_data in USERS.items():
        # Check if user already exists
        existing_user = session.get(User, user_data["id"])
        if existing_user:
            print(f"  User {user_key} already exists, skipping...")
            continue
        
        # Create new user
        user = User(
            id=uuid.UUID(user_data["id"]),
            organization_id=uuid.UUID(user_data["organization_id"]) if user_data["organization_id"] else uuid.uuid4(),
            full_name=user_data["full_name"],
            email=user_data["email"],
            hashed_password=user_data["hashed_password"],
            role=user_data["role"],
            contact_telephone=user_data["contact_telephone"],
            is_special_user=user_data["is_special_user"],
            special_user_type=user_data["special_user_type"],
            created_at=datetime.now()
        )
        
        session.add(user)
        print(f"  Created user: {user.full_name} ({user.role})")
    
    session.commit()
    print(f"  Loaded {len(USERS)} users")


def load_receipts(session: Session):
    """Load receipt test data."""
    print("Loading receipts...")
    
    for receipt_key, receipt_data in RECEIPTS.items():
        # Check if receipt already exists
        existing_receipt = session.get(Receipt, receipt_data["id"])
        if existing_receipt:
            print(f"  Receipt {receipt_key} already exists, skipping...")
            continue
        
        # Create new receipt
        receipt = Receipt(
            id=uuid.UUID(receipt_data["id"]),
            user_id=uuid.UUID(receipt_data["user_id"]),
            organization_id=uuid.UUID(receipt_data["organization_id"]),
            image_url=receipt_data["image_url"],
            vendor_name=receipt_data["vendor_name"],
            purchase_date=receipt_data["purchase_date"],
            county=receipt_data["county"],
            subtotal_amount=receipt_data["subtotal_amount"],
            tax_amount=receipt_data["tax_amount"],
            total_amount=receipt_data["total_amount"],
            expense_category=receipt_data["expense_category"],
            status=receipt_data["status"],
            is_donation=receipt_data["is_donation"],
            payment_method=receipt_data["payment_method"],
            payment_reference=receipt_data["payment_reference"],
            payment_proof_url=receipt_data["payment_proof_url"],
            submitted_at=receipt_data["submitted_at"],
            approved_at=receipt_data["approved_at"]
        )
        
        session.add(receipt)
        print(f"  Created receipt: {receipt.vendor_name} - ${receipt.total_amount}")
    
    session.commit()
    print(f"  Loaded {len(RECEIPTS)} receipts")


def load_tax_breakdowns(session: Session):
    """Load tax breakdown test data."""
    print("Loading tax breakdowns...")
    
    total_breakdowns = 0
    for breakdown_key, breakdowns in TAX_BREAKDOWNS.items():
        for breakdown_data in breakdowns:
            # Check if breakdown already exists
            existing_breakdown = session.get(ReceiptTaxBreakdown, breakdown_data["id"])
            if existing_breakdown:
                print(f"  Tax breakdown {breakdown_key} already exists, skipping...")
                continue
            
            # Create new tax breakdown
            breakdown = ReceiptTaxBreakdown(
                id=uuid.UUID(breakdown_data["id"]),
                receipt_id=uuid.UUID(breakdown_data["receipt_id"]),
                tax_type=breakdown_data["tax_type"],
                amount=breakdown_data["amount"]
            )
            
            session.add(breakdown)
            total_breakdowns += 1
    
    session.commit()
    print(f"  Loaded {total_breakdowns} tax breakdowns")


def load_payment_transactions(session: Session):
    """Load payment transaction test data."""
    print("Loading payment transactions...")
    
    for transaction_key, transaction_data in PAYMENT_TRANSACTIONS.items():
        # Check if transaction already exists
        existing_transaction = session.get(PaymentTransaction, transaction_data["id"])
        if existing_transaction:
            print(f"  Payment transaction {transaction_key} already exists, skipping...")
            continue
        
        # Create new payment transaction
        transaction = PaymentTransaction(
            id=uuid.UUID(transaction_data["id"]),
            organization_id=uuid.UUID(transaction_data["organization_id"]),
            transaction_date=transaction_data["transaction_date"],
            amount=transaction_data["amount"],
            reference_id=transaction_data["reference_id"],
            receipt_id=uuid.UUID(transaction_data["receipt_id"]) if transaction_data["receipt_id"] else None
        )
        
        session.add(transaction)
        print(f"  Created payment transaction: {transaction.reference_id} - ${transaction.amount}")
    
    session.commit()
    print(f"  Loaded {len(PAYMENT_TRANSACTIONS)} payment transactions")


def load_feedback(session: Session):
    """Load feedback test data."""
    print("Loading feedback...")
    
    for feedback_key, feedback_data in FEEDBACK.items():
        # Check if feedback already exists
        existing_feedback = session.get(Feedback, feedback_data["id"])
        if existing_feedback:
            print(f"  Feedback {feedback_key} already exists, skipping...")
            continue
        
        # Create new feedback
        feedback = Feedback(
            id=uuid.UUID(feedback_data["id"]),
            user_id=uuid.UUID(feedback_data["user_id"]),
            organization_id=uuid.UUID(feedback_data["organization_id"]),
            category=feedback_data["category"],
            description=feedback_data["description"],
            device_info=feedback_data["device_info"],
            status=feedback_data["status"],
            created_at=feedback_data["created_at"]
        )
        
        session.add(feedback)
        print(f"  Created feedback: {feedback.category} - {feedback.description[:50]}...")
    
    session.commit()
    print(f"  Loaded {len(FEEDBACK)} feedback entries")


def load_all_test_data():
    """Load all test data into the database."""
    print("🚀 Loading test data into database...")
    
    # Create database engine
    engine = create_test_engine()
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    
    # Load data in dependency order
    with Session(engine) as session:
        try:
            load_organizations(session)
            load_users(session)
            load_receipts(session)
            load_tax_breakdowns(session)
            load_payment_transactions(session)
            load_feedback(session)
            
            print("\n✅ All test data loaded successfully!")
            
            # Print summary
            print("\n📊 Test Data Summary:")
            print(f"  Organizations: {len(ORGANIZATIONS)}")
            print(f"  Users: {len(USERS)}")
            print(f"  Receipts: {len(RECEIPTS)}")
            print(f"  Tax Breakdowns: {sum(len(breakdowns) for breakdowns in TAX_BREAKDOWNS.values())}")
            print(f"  Payment Transactions: {len(PAYMENT_TRANSACTIONS)}")
            print(f"  Feedback: {len(FEEDBACK)}")
            
        except Exception as e:
            print(f"\n❌ Error loading test data: {e}")
            session.rollback()
            raise


def clear_test_data():
    """Clear all test data from the database."""
    print("🗑️ Clearing test data from database...")
    
    engine = create_test_engine()
    
    with Session(engine) as session:
        try:
            # Delete in reverse dependency order
            session.query(Feedback).delete()
            session.query(ReceiptTaxBreakdown).delete()
            session.query(PaymentTransaction).delete()
            session.query(Receipt).delete()
            session.query(User).delete()
            session.query(Organization).delete()
            
            session.commit()
            print("✅ All test data cleared successfully!")
            
        except Exception as e:
            print(f"❌ Error clearing test data: {e}")
            session.rollback()
            raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_test_data()
    else:
        load_all_test_data() 