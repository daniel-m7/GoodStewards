"""
Automated cleanup of duplicate tables in the database.

This script removes the manually created tables (plural names) and keeps
only the SQLModel-generated tables (singular names) which is the correct convention.
"""

import os
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def cleanup_duplicate_tables():
    """Remove duplicate tables and keep only SQLModel tables."""
    print("🧹 Cleaning up duplicate tables...")
    
    # Use the same connection details
    database_url = "postgresql://postgres:postgres@localhost:5432/goodstewards"
    
    print(f"🔗 Connecting to: {database_url}")
    
    try:
        # Connect to database
        with psycopg.connect(database_url) as conn:
            print("✅ Successfully connected to database!")
            
            with conn.cursor() as cur:
                # Check what tables exist
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()
                
                print(f"\n📋 Current tables:")
                for table in tables:
                    table_name = table[0]
                    cur.execute(f"SELECT COUNT(*) FROM \"{table_name}\";")
                    count = cur.fetchone()[0]
                    print(f"  - {table_name}: {count} rows")
                
                # Define which tables to keep (SQLModel convention)
                tables_to_keep = [
                    "user",           # SQLModel: User
                    "receipt",        # SQLModel: Receipt  
                    "organization",   # SQLModel: Organization
                    "receipttaxbreakdown",  # SQLModel: ReceiptTaxBreakdown
                    "paymenttransaction", # SQLModel: PaymentTransaction (has data)
                    "feedback"        # SQLModel: Feedback
                ]
                
                # Define which tables to remove (manual SQL convention or duplicates)
                tables_to_remove = [
                    "users",          # Manual: CREATE TABLE users
                    "receipts",       # Manual: CREATE TABLE receipts
                    "organizations",  # Manual: CREATE TABLE organizations
                    "receipt_tax_breakdowns",  # Manual: CREATE TABLE receipt_tax_breakdowns
                    "payment_transactions"  # Empty duplicate table
                ]
                
                print(f"\n🗑️ Tables to remove (manual SQL):")
                for table in tables_to_remove:
                    if table in [t[0] for t in tables]:
                        print(f"  - {table}")
                
                print(f"\n✅ Tables to keep (SQLModel):")
                for table in tables_to_keep:
                    if table in [t[0] for t in tables]:
                        print(f"  - {table}")
                
                # Remove duplicate tables
                print(f"\n🗑️ Removing duplicate tables...")
                for table in tables_to_remove:
                    if table in [t[0] for t in tables]:
                        try:
                            cur.execute(f"DROP TABLE IF EXISTS \"{table}\" CASCADE;")
                            print(f"  ✅ Removed: {table}")
                        except Exception as e:
                            print(f"  ❌ Error removing {table}: {e}")
                
                conn.commit()
                
                # Verify cleanup
                print(f"\n🔍 Verifying cleanup...")
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                remaining_tables = cur.fetchall()
                
                print(f"📋 Remaining tables:")
                for table in remaining_tables:
                    table_name = table[0]
                    cur.execute(f"SELECT COUNT(*) FROM \"{table_name}\";")
                    count = cur.fetchone()[0]
                    print(f"  - {table_name}: {count} rows")
                
                print(f"\n✅ Cleanup completed!")
                print(f"💡 Now use these table names:")
                print(f"  - SELECT * FROM \"user\";")
                print(f"  - SELECT * FROM receipt;")
                print(f"  - SELECT * FROM organization;")
                print(f"  - SELECT * FROM paymenttransaction;")
                        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    cleanup_duplicate_tables() 