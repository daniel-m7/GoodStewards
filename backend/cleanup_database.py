#!/usr/bin/env python3
"""
Database cleanup script for GoodStewards
Clears all data from the database for testing purposes
"""

import asyncio
import os
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import select

from app.models.models import Receipt, ReceiptTaxBreakdown, User, Organization, Feedback, PaymentTransaction
from app.core.config import settings

async def cleanup_database():
    """Clear all data from the database."""
    print("Starting database cleanup...")
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Clear feedback first (it references users)
            print("Clearing feedback...")
            result = await session.exec(select(Feedback))
            feedbacks = result.all()
            for feedback in feedbacks:
                await session.delete(feedback)
            print(f"Deleted {len(feedbacks)} feedback records")
            
            # Clear payment transactions (they reference organizations)
            print("Clearing payment transactions...")
            result = await session.exec(select(PaymentTransaction))
            payments = result.all()
            for payment in payments:
                await session.delete(payment)
            print(f"Deleted {len(payments)} payment transactions")
            
            # Clear receipts and tax breakdowns (they depend on users and organizations)
            print("Clearing receipts and tax breakdowns...")
            result = await session.exec(select(ReceiptTaxBreakdown))
            tax_breakdowns = result.all()
            for breakdown in tax_breakdowns:
                await session.delete(breakdown)
            print(f"Deleted {len(tax_breakdowns)} tax breakdowns")
            
            result = await session.exec(select(Receipt))
            receipts = result.all()
            for receipt in receipts:
                await session.delete(receipt)
            print(f"Deleted {len(receipts)} receipts")
            
            # Clear users
            print("Clearing users...")
            result = await session.exec(select(User))
            users = result.all()
            for user in users:
                await session.delete(user)
            print(f"Deleted {len(users)} users")
            
            # Clear organizations
            print("Clearing organizations...")
            result = await session.exec(select(Organization))
            organizations = result.all()
            for organization in organizations:
                await session.delete(organization)
            print(f"Deleted {len(organizations)} organizations")
            
            # Commit all changes
            await session.commit()
            print("Database cleanup completed successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"Error during cleanup: {e}")
            raise
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(cleanup_database()) 