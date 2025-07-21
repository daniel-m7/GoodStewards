"""
Check the user table specifically.
"""

import os
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_user_table():
    """Check the user table specifically."""
    print("🔍 Checking user table...")
    
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
            with conn.cursor() as cur:
                # Check user table
                print("\n👥 Checking 'user' table:")
                cur.execute("SELECT COUNT(*) FROM \"user\";")
                user_count = cur.fetchone()[0]
                print(f"  📊 Total users: {user_count}")
                
                if user_count > 0:
                    cur.execute("SELECT * FROM \"user\";")
                    users = cur.fetchall()
                    
                    # Get column names
                    cur.execute("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'user' 
                        ORDER BY ordinal_position;
                    """)
                    columns = [col[0] for col in cur.fetchall()]
                    print(f"  📋 Columns: {', '.join(columns)}")
                    
                    print(f"  📄 All users:")
                    for i, user in enumerate(users):
                        print(f"    User {i+1}: {user}")
                
                # Check users table (plural)
                print("\n👥 Checking 'users' table:")
                cur.execute("SELECT COUNT(*) FROM users;")
                users_count = cur.fetchone()[0]
                print(f"  📊 Total users: {users_count}")
                
                if users_count > 0:
                    cur.execute("SELECT * FROM users LIMIT 5;")
                    users = cur.fetchall()
                    print(f"  📄 Sample users:")
                    for i, user in enumerate(users):
                        print(f"    User {i+1}: {user}")
                        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_user_table() 