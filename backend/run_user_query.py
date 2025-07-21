"""
Run the exact SQL query the user is running.
"""

import os
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_user_query():
    """Run the exact query: SELECT * FROM users;"""
    print("🔍 Running your exact query: SELECT * FROM users;")
    
    # Use the same connection details as the user
    database_url = "postgresql://postgres:postgres@localhost:5432/goodstewards"
    
    print(f"🔗 Connecting to: {database_url}")
    
    try:
        # Connect to database
        with psycopg.connect(database_url) as conn:
            print("✅ Successfully connected to database!")
            
            with conn.cursor() as cur:
                # Run the exact query
                print("\n📋 Executing: SELECT * FROM users;")
                cur.execute("SELECT * FROM users;")
                rows = cur.fetchall()
                
                print(f"\n📊 Results:")
                print(f"  Number of rows returned: {len(rows)}")
                
                if len(rows) == 0:
                    print("  ❌ No rows found - table is empty")
                else:
                    print("  ✅ Rows found:")
                    for i, row in enumerate(rows):
                        print(f"    Row {i+1}: {row}")
                
                # Also check the user table (singular) for comparison
                print(f"\n🔍 For comparison, checking 'user' table:")
                cur.execute("SELECT COUNT(*) FROM \"user\";")
                user_count = cur.fetchone()[0]
                print(f"  📊 Rows in 'user' table: {user_count}")
                
                if user_count > 0:
                    cur.execute("SELECT id, full_name, email, role FROM \"user\" LIMIT 3;")
                    users = cur.fetchall()
                    print(f"  📄 Sample users from 'user' table:")
                    for i, user in enumerate(users):
                        print(f"    User {i+1}: {user[1]} ({user[2]}) - {user[3]}")
                        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_user_query() 