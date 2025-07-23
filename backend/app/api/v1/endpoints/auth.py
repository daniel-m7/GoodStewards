from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import verify_password, create_access_token, get_current_active_user
from app.core.config import settings
from app.core.db import get_session
from app.models.models import User

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Find user by email
    statement = select(User).where(User.email == form_data.username)
    result = await session.exec(statement)
    user = result.first()
    
    if not user or not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "organization_id": str(user.organization_id)
        }
    }

from app.models.models import Organization, Role
from pydantic import BaseModel, validator
from typing import Optional
import uuid

class OrganizationRegistration(BaseModel):
    name: str
    fein: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

class UserRegistration(BaseModel):
    full_name: str
    email: str
    password: str
    organization_id: Optional[uuid.UUID] = None
    organization: Optional[OrganizationRegistration] = None

    @validator('organization', always=True)
    def check_organization_or_id(cls, v, values):
        if values.get('organization_id') is None and v is None:
            raise ValueError('Either organization_id or organization must be provided')
        if values.get('organization_id') is not None and v is not None:
            raise ValueError('Provide either organization_id or organization, not both')
        return v

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user_and_organization(
    registration_data: UserRegistration,
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new user and optionally a new organization.
    - If `organization_id` is provided, the user joins an existing organization.
    - If `organization` data is provided, a new organization is created, and the user becomes its treasurer.
    """
    # Check if user already exists
    result = await session.exec(select(User).where(User.email == registration_data.email))
    existing_user = result.first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists."
        )

    from app.core.auth import get_password_hash
    hashed_password = get_password_hash(registration_data.password)
    
    organization_id: uuid.UUID
    user_role = Role.member

    if registration_data.organization:
        # Create a new organization
        org_data = registration_data.organization
        
        # Check if an organization with the same FEIN already exists
        if org_data.fein:
            result = await session.exec(select(Organization).where(Organization.fein == org_data.fein))
            existing_org = result.first()
            if existing_org:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Organization with FEIN {org_data.fein} already exists."
                )

        new_organization = Organization(
            name=org_data.name,
            fein=org_data.fein,
            address=org_data.address,
            city=org_data.city,
            state=org_data.state,
            zip_code=org_data.zip_code
        )
        session.add(new_organization)
        await session.commit()
        await session.refresh(new_organization)
        organization_id = new_organization.id
        user_role = Role.treasurer # First user becomes treasurer
    
    elif registration_data.organization_id:
        # Join an existing organization
        organization = await session.get(Organization, registration_data.organization_id)
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization with ID {registration_data.organization_id} not found."
            )
        organization_id = registration_data.organization_id
    else:
        # This case should be prevented by the Pydantic validator, but as a safeguard:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must either provide an `organization_id` to join or `organization` data to create one."
        )

    # Create the new user
    new_user = User(
        full_name=registration_data.full_name,
        email=registration_data.email,
        hashed_password=hashed_password,
        organization_id=organization_id,
        role=user_role
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {
        "message": "User and organization registered successfully.",
        "user_id": new_user.id,
        "organization_id": organization_id,
        "user_role": user_role
    }

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information.
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "organization_id": str(current_user.organization_id)
    } 