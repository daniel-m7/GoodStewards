"""
Check all tables in the database to see where the data is.
"""

import os
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_all_tables():
    """Check all tables and their data."""
    print("🔍 Checking all tables in database...")
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ No DATABASE_URL found in environment")
        return
    
    # Convert async URL to sync URL if needed
    if database_url.startswith("postgresql+psycopg_async://"):
        database_url = database_url.replace("postgresql+psycopg_async://", "postgresql://")
    
    # Replace Docker container name with localhost when running outside Docker
    if "db:5432" in database_url:
        database_url = database_url.replace("db:5432", "localhost:5432")
    
    try:
        # Connect to database
        with psycopg.connect(database_url) as conn:
            print("✅ Successfully connected to database!")
            
            with conn.cursor() as cur:
                # Get all tables
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()
                
                print(f"\n📋 Found {len(tables)} tables:")
                for table in tables:
                    table_name = table[0]
                    print(f"\n🔍 Checking table: {table_name}")
                    
                    # Get row count
                    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
                    count = cur.fetchone()[0]
                    print(f"  📊 Row count: {count}")
                    
                    if count > 0:
                        # Get sample data
                        cur.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                        rows = cur.fetchall()
                        
                        # Get column names
                        cur.execute(f"""
                            SELECT column_name 
                            FROM information_schema.columns 
                            WHERE table_name = '{table_name}' 
                            ORDER BY ordinal_position;
                        """)
                        columns = [col[0] for col in cur.fetchall()]
                        
                        print(f"  📋 Columns: {', '.join(columns)}")
                        print(f"  📄 Sample data:")
                        for i, row in enumerate(rows):
                            print(f"    Row {i+1}: {row}")
                    else:
                        print(f"  ❌ Table is empty")
                        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_all_tables() 