"""
Setup database tables and load test data.
"""

import os
import asyncio
from sqlmodel import create_all, SQLModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all models to register them
from app.models.models import Organization, User, Receipt, ReceiptTaxBreakdown, PaymentTransaction, Feedback

async def setup_database():
    """Create tables and load test data."""
    print("🔧 Setting up database...")
    
    # Import database engine
    from app.core.database import engine
    
    # Create all tables
    print("📋 Creating database tables...")
    create_all(engine)
    print("✅ Tables created successfully!")
        
    print("🎉 Database setup complete!")

if __name__ == "__main__":
    asyncio.run(setup_database()) 