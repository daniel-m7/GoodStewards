from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.auth import verify_password, create_access_token, get_current_active_user
from app.core.config import settings
from app.core.db import get_session
from app.models.models import User

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Find user by email
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
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

@router.post("/register")
async def register(
    email: str,
    password: str,
    full_name: str,
    organization_id: str,
    session: Session = Depends(get_session)
):
    """
    Register a new user.
    """
    # Check if user already exists
    statement = select(User).where(User.email == email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    from app.core.auth import get_password_hash
    hashed_password = get_password_hash(password)
    
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        organization_id=organization_id,
        role="member"  # Default role
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {
        "message": "User created successfully",
        "user_id": str(new_user.id)
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