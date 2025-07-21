"""
Check database connection and show data directly.
"""

import os
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_database():
    """Check database connection and show data."""
    print("🔍 Checking database connection...")
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ No DATABASE_URL found in environment")
        return
    
    print(f"📋 DATABASE_URL: {database_url}")
    
    # Convert async URL to sync URL if needed
    if database_url.startswith("postgresql+psycopg_async://"):
        database_url = database_url.replace("postgresql+psycopg_async://", "postgresql://")
    
    # Replace Docker container name with localhost when running outside Docker
    if "db:5432" in database_url:
        database_url = database_url.replace("db:5432", "localhost:5432")
        print("🔄 Replaced 'db' with 'localhost' for local connection")
    
    print(f"🔗 Final connection string: {database_url}")
    
    try:
        # Connect to database
        with psycopg.connect(database_url) as conn:
            print("✅ Successfully connected to database!")
            
            # Get database info
            with conn.cursor() as cur:
                cur.execute("SELECT current_database(), current_user, version();")
                db_info = cur.fetchone()
                print(f"📊 Database: {db_info[0]}")
                print(f"👤 User: {db_info[1]}")
                print(f"🔧 Version: {db_info[2].split(',')[0]}")
                
                # Check if tables exist
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()
                print(f"\n📋 Tables in database:")
                for table in tables:
                    print(f"  - {table[0]}")
                
                # Check users table specifically
                print(f"\n👥 Checking users table...")
                cur.execute("SELECT COUNT(*) FROM users;")
                user_count = cur.fetchone()[0]
                print(f"  Total users: {user_count}")
                
                if user_count > 0:
                    cur.execute("SELECT id, full_name, email, role FROM users LIMIT 5;")
                    users = cur.fetchall()
                    print(f"  Sample users:")
                    for user in users:
                        print(f"    - {user[1]} ({user[2]}) - {user[3]}")
                else:
                    print("  ❌ No users found in table")
                    
                # Check organizations table
                print(f"\n🏢 Checking organizations table...")
                cur.execute("SELECT COUNT(*) FROM organizations;")
                org_count = cur.fetchone()[0]
                print(f"  Total organizations: {org_count}")
                
                if org_count > 0:
                    cur.execute("SELECT id, name, fein FROM organizations LIMIT 3;")
                    orgs = cur.fetchall()
                    print(f"  Sample organizations:")
                    for org in orgs:
                        print(f"    - {org[1]} (FEIN: {org[2]})")
                else:
                    print("  ❌ No organizations found in table")
                    
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        print(f"💡 Make sure the database is running and accessible")

if __name__ == "__main__":
    check_database() 