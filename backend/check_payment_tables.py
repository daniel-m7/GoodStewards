"""
Check the contents of payment-related tables to identify duplicates.
"""

import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_payment_tables():
    """Check both payment-related tables."""
    print("🔍 Checking payment-related tables...")
    
    database_url = "postgresql://postgres:postgres@localhost:5432/goodstewards"
    
    try:
        with psycopg.connect(database_url) as conn:
            print("✅ Connected to database!")
            
            with conn.cursor() as cur:
                # Check payment_transactions table
                print(f"\n📋 Table: payment_transactions")
                cur.execute("SELECT COUNT(*) FROM payment_transactions;")
                count = cur.fetchone()[0]
                print(f"  Rows: {count}")
                
                if count > 0:
                    cur.execute("SELECT * FROM payment_transactions LIMIT 3;")
                    rows = cur.fetchall()
                    print(f"  Sample data:")
                    for i, row in enumerate(rows, 1):
                        print(f"    Row {i}: {row}")
                
                # Check paymenttransaction table
                print(f"\n📋 Table: paymenttransaction")
                cur.execute("SELECT COUNT(*) FROM paymenttransaction;")
                count = cur.fetchone()[0]
                print(f"  Rows: {count}")
                
                if count > 0:
                    cur.execute("SELECT * FROM paymenttransaction LIMIT 3;")
                    rows = cur.fetchall()
                    print(f"  Sample data:")
                    for i, row in enumerate(rows, 1):
                        print(f"    Row {i}: {row}")
                
                # Check table schemas
                print(f"\n🔍 Table schemas:")
                
                print(f"\n  payment_transactions schema:")
                cur.execute("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'payment_transactions' 
                    ORDER BY ordinal_position;
                """)
                columns = cur.fetchall()
                for col in columns:
                    print(f"    {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
                
                print(f"\n  paymenttransaction schema:")
                cur.execute("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'paymenttransaction' 
                    ORDER BY ordinal_position;
                """)
                columns = cur.fetchall()
                for col in columns:
                    print(f"    {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
                        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_payment_tables() 