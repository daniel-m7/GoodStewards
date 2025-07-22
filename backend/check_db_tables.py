#!/usr/bin/env python3
"""
Check database table structure to verify correct table names.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_database_tables():
    """Check and display current database table structure."""
    import psycopg
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL environment variable is not set")
        return
    
    # Convert SQLAlchemy URL to psycopg connection string
    if DATABASE_URL.startswith("postgresql+psycopg_async://"):
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
            
            conn_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        else:
            conn_string = DATABASE_URL
    else:
        conn_string = DATABASE_URL
    
    try:
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                # Get all tables
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_name;
                """)
                
                tables = [row[0] for row in cur.fetchall()]
                
                print("📋 Current database tables:")
                print("=" * 50)
                
                # Define expected tables (from Alembic migrations)
                expected_tables = {
                    'organization': 'Organization model',
                    'user': 'User model', 
                    'receipt': 'Receipt model',
                    'receipttaxbreakdown': 'ReceiptTaxBreakdown model',
                    'paymenttransaction': 'PaymentTransaction model',
                    'feedback': 'Feedback model'
                }
                
                for table in tables:
                    if table in expected_tables:
                        # Get row count
                        cur.execute(f"SELECT COUNT(*) FROM {table};")
                        count = cur.fetchone()[0]
                        print(f"✅ {table:<20} ({expected_tables[table]:<25}) - {count} rows")
                    else:
                        # Get row count for unexpected tables
                        cur.execute(f"SELECT COUNT(*) FROM {table};")
                        count = cur.fetchone()[0]
                        print(f"⚠️  {table:<20} (UNEXPECTED TABLE)           - {count} rows")
                
                print("=" * 50)
                
                # Check for duplicates
                duplicate_tables = []
                for table in tables:
                    if table not in expected_tables:
                        if table.endswith('s') and table[:-1] in expected_tables:
                            duplicate_tables.append(table)
                        elif table in ['organizations', 'users', 'receipts']:
                            duplicate_tables.append(table)
                
                if duplicate_tables:
                    print(f"\n⚠️  Found {len(duplicate_tables)} duplicate tables:")
                    for table in duplicate_tables:
                        print(f"   - {table}")
                    print("\n💡 Run cleanup_duplicate_tables.py to remove duplicates")
                else:
                    print("\n✅ No duplicate tables found!")
                
                # Show table structure for each expected table
                print(f"\n🔍 Table structure details:")
                print("=" * 50)
                
                for table in expected_tables:
                    if table in tables:
                        cur.execute(f"""
                            SELECT column_name, data_type, is_nullable, column_default
                            FROM information_schema.columns 
                            WHERE table_name = '{table}' 
                            AND table_schema = 'public'
                            ORDER BY ordinal_position;
                        """)
                        
                        columns = cur.fetchall()
                        print(f"\n📋 {table} ({expected_tables[table]}):")
                        for col in columns:
                            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                            default = f" DEFAULT {col[3]}" if col[3] else ""
                            print(f"   - {col[0]:<20} {col[1]:<15} {nullable}{default}")
                
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return

if __name__ == "__main__":
    check_database_tables() 