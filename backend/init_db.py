#!/usr/bin/env python3
"""
Database initialization script.
This script can be run manually to initialize the database with tables.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import create_tables
from alembic.config import Config
from alembic import command

def main():
    """Initialize the database with tables and run migrations."""
    load_dotenv()
    
    print("Initializing database...")
    
    # Create tables using the manual script
    try:
        create_tables()
        print("✓ Tables created successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not create tables manually: {e}")
    
    # Run Alembic migrations
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("✓ Alembic migrations completed successfully")
    except Exception as e:
        print(f"✗ Error running Alembic migrations: {e}")
        sys.exit(1)
    
    print("Database initialization completed!")

if __name__ == "__main__":
    main() 