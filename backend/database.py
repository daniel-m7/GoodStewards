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
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id UUID PRIMARY KEY,
                name VARCHAR,
                fein VARCHAR,
                ntee_code VARCHAR,
                address VARCHAR,
                city VARCHAR,
                state VARCHAR,
                zip_code VARCHAR,
                created_at TIMESTAMPTZ
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY,
                organization_id UUID REFERENCES organizations(id),
                full_name VARCHAR,
                email VARCHAR UNIQUE,
                role VARCHAR,
                created_at TIMESTAMPTZ
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id UUID PRIMARY KEY,
                user_id UUID REFERENCES users(id),
                organization_id UUID REFERENCES organizations(id),
                image_url VARCHAR,
                vendor_name VARCHAR,
                purchase_date VARCHAR,
                county VARCHAR,
                subtotal_amount DECIMAL,
                tax_amount DECIMAL,
                total_amount DECIMAL,
                expense_category VARCHAR,
                status VARCHAR,
                is_donation BOOLEAN,
                payment_method VARCHAR,
                payment_reference VARCHAR,
                payment_proof_url VARCHAR,
                submitted_at TIMESTAMPTZ,
                approved_at TIMESTAMPTZ
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS payment_transactions (
                id UUID PRIMARY KEY,
                organization_id UUID REFERENCES organizations(id),
                transaction_date DATE,
                amount DECIMAL,
                reference_id VARCHAR,
                receipt_id UUID REFERENCES receipts(id)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS receipt_tax_breakdowns (
                id UUID PRIMARY KEY,
                receipt_id UUID REFERENCES receipts(id),
                tax_type VARCHAR,
                amount DECIMAL
            );
        """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables() 