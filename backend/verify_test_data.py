"""
Verify test data in the database for GoodStewards application.

This script checks that all test data was loaded correctly and displays
a summary of what's in the database.
"""

import os
from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv

from app.models.models import (
    Organization, User, Receipt, ReceiptTaxBreakdown, 
    PaymentTransaction, Feedback
)

# Load environment variables
load_dotenv()


def create_test_engine():
    """Create a database engine."""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("⚠️  No DATABASE_URL found")
        return None
    
    # Convert async URL to sync URL if needed
    if database_url.startswith("postgresql+psycopg_async://"):
        database_url = database_url.replace("postgresql+psycopg_async://", "postgresql://")
    
    # Replace Docker container name with localhost when running outside Docker
    if "db:5432" in database_url:
        database_url = database_url.replace("db:5432", "localhost:5432")
    
    print(f"🔗 Connecting to database: {database_url}")
    
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
    )
    return engine


def verify_organizations(session: Session):
    """Verify organizations in the database."""
    print("\n🏢 Organizations:")
    organizations = session.exec(select(Organization)).all()
    
    if not organizations:
        print("  ❌ No organizations found")
        return
    
    for org in organizations:
        print(f"  ✅ {org.name} (FEIN: {org.fein})")
        print(f"      Address: {org.address}, {org.city}, {org.state} {org.zip_code}")


def verify_users(session: Session):
    """Verify users in the database."""
    print("\n👥 Users:")
    users = session.exec(select(User)).all()
    
    if not users:
        print("  ❌ No users found")
        return
    
    for user in users:
        role_info = f"({user.role})"
        if user.is_special_user:
            role_info += f" - Special: {user.special_user_type}"
        
        print(f"  ✅ {user.full_name} {role_info}")
        if user.email:
            print(f"      Email: {user.email}")
        if user.contact_telephone:
            print(f"      Phone: {user.contact_telephone}")


def verify_receipts(session: Session):
    """Verify receipts in the database."""
    print("\n🧾 Receipts:")
    receipts = session.exec(select(Receipt)).all()
    
    if not receipts:
        print("  ❌ No receipts found")
        return
    
    for receipt in receipts:
        donation_info = " (DONATION)" if receipt.is_donation else ""
        print(f"  ✅ {receipt.vendor_name} - ${receipt.total_amount}{donation_info}")
        print(f"      Status: {receipt.status}, Category: {receipt.expense_category}")
        print(f"      Date: {receipt.purchase_date}, County: {receipt.county}")


def verify_tax_breakdowns(session: Session):
    """Verify tax breakdowns in the database."""
    print("\n💰 Tax Breakdowns:")
    breakdowns = session.exec(select(ReceiptTaxBreakdown)).all()
    
    if not breakdowns:
        print("  ❌ No tax breakdowns found")
        return
    
    for breakdown in breakdowns:
        print(f"  ✅ {breakdown.tax_type}: ${breakdown.amount}")


def verify_payment_transactions(session: Session):
    """Verify payment transactions in the database."""
    print("\n💳 Payment Transactions:")
    transactions = session.exec(select(PaymentTransaction)).all()
    
    if not transactions:
        print("  ❌ No payment transactions found")
        return
    
    for transaction in transactions:
        print(f"  ✅ {transaction.reference_id} - ${transaction.amount}")
        print(f"      Date: {transaction.transaction_date}")


def verify_feedback(session: Session):
    """Verify feedback in the database."""
    print("\n💬 Feedback:")
    feedback_entries = session.exec(select(Feedback)).all()
    
    if not feedback_entries:
        print("  ❌ No feedback found")
        return
    
    for feedback in feedback_entries:
        print(f"  ✅ {feedback.category}: {feedback.description[:50]}...")
        print(f"      Status: {feedback.status}")


def verify_relationships(session: Session):
    """Verify relationships between entities."""
    print("\n🔗 Relationships:")
    
    # Check organization-user relationships
    orgs = session.exec(select(Organization)).all()
    for org in orgs:
        users = session.exec(select(User).where(User.organization_id == org.id)).all()
        print(f"  📊 {org.name}: {len(users)} users")
    
    # Check user-receipt relationships
    users = session.exec(select(User)).all()
    for user in users:
        receipts = session.exec(select(Receipt).where(Receipt.user_id == user.id)).all()
        if receipts:
            print(f"  📊 {user.full_name}: {len(receipts)} receipts")


def verify_all_data():
    """Verify all test data in the database."""
    print("🔍 Verifying test data in database...")
    
    engine = create_test_engine()
    if not engine:
        print("❌ Could not create database engine")
        return
    
    with Session(engine) as session:
        try:
            verify_organizations(session)
            verify_users(session)
            verify_receipts(session)
            verify_tax_breakdowns(session)
            verify_payment_transactions(session)
            verify_feedback(session)
            verify_relationships(session)
            
            print("\n✅ Database verification completed!")
            
        except Exception as e:
            print(f"\n❌ Error verifying data: {e}")
            raise


if __name__ == "__main__":
    verify_all_data() 