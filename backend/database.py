import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    # Convert SQLAlchemy URL to psycopg connection string if needed
    if DATABASE_URL.startswith("postgresql+psycopg_async://"):
        # Extract components from SQLAlchemy URL
        url = DATABASE_URL.replace("postgresql+psycopg_async://", "")
        if "@" in url:
            auth, rest = url.split("@", 1)
            user, password = auth.split(":", 1)
            host_port_db = rest.split("/", 1)
            host_port = host_port_db[0]
            db_name = host_port_db[1] if len(host_port_db) > 1 else "goodstewards"
            
            if ":" in host_port:
                host, port = host_port.split(":", 1)
            else:
                host, port = host_port, "5432"
            
            # Build standard PostgreSQL connection string
            conn_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        else:
            conn_string = DATABASE_URL
    else:
        conn_string = DATABASE_URL
    
    return psycopg.connect(conn_string)

def create_tables():
    """
    DEPRECATED: This function is no longer needed.
    
    SQLModel automatically creates tables based on the model definitions in app/models/models.py.
    The tables are created with singular names following SQLModel conventions:
    - organization (from Organization class)
    - user (from User class) 
    - receipt (from Receipt class)
    - receipttaxbreakdown (from ReceiptTaxBreakdown class)
    - payment_transactions (from PaymentTransaction class)
    - feedback (from Feedback class)
    
    To create tables, use SQLModel's create_all() function instead:
    from sqlmodel import create_all
    from app.models.models import *
    create_all(engine)
    """
    print("⚠️  DEPRECATED: Use SQLModel's create_all() instead of manual table creation")
    print("💡 Tables are automatically created by SQLModel with singular names")
    print("📋 Correct table names: organization, user, receipt, receipttaxbreakdown, payment_transactions, feedback")

if __name__ == "__main__":
    create_tables() 