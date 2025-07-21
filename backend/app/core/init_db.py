from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
from app.models.models import Organization, User, Role
from app.core.auth import get_password_hash

def init_db():
    """Initialize the database with tables and sample data."""
    # Create engine
    engine = create_engine(settings.DATABASE_URL, echo=True)
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    
    # Create sample data
    with Session(engine) as session:
        # Check if sample organization already exists
        existing_org = session.exec(
            "SELECT * FROM organization WHERE name = 'Sample Non-Profit'"
        ).first()
        
        if not existing_org:
            # Create sample organization
            org = Organization(
                name="Sample Non-Profit",
                fein="12-3456789",
                ntee_code="A01",
                address="123 Main St",
                city="Anytown",
                state="NC",
                zip_code="12345"
            )
            session.add(org)
            session.commit()
            session.refresh(org)
            
            # Create sample treasurer
            treasurer = User(
                email="treasurer@samplenonprofit.org",
                hashed_password=get_password_hash("password123"),
                full_name="John Treasurer",
                role=Role.treasurer,
                organization_id=org.id
            )
            session.add(treasurer)
            
            # Create sample member
            member = User(
                email="member@samplenonprofit.org",
                hashed_password=get_password_hash("password123"),
                full_name="Jane Member",
                role=Role.member,
                organization_id=org.id
            )
            session.add(member)
            
            session.commit()
            print("Sample data created successfully!")
        else:
            print("Sample data already exists.")

if __name__ == "__main__":
    init_db() 