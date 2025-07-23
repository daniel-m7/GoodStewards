from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import or_
from uuid import UUID

from app.core.auth import get_current_active_user, require_treasurer_role
from app.core.db import get_session
from app.models.models import User, Organization, SpecialUserType, Role

router = APIRouter()

@router.get("/health-check")
async def health_check():
    """
    Check if the API is running.
    """
    return {"status": "ok"}

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current user's profile information.
    """
    return {
        "id": str(current_user.id),
        "organization_id": str(current_user.organization_id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "contact_telephone": current_user.contact_telephone,
        "is_special_user": current_user.is_special_user,
        "special_user_type": current_user.special_user_type,
        "created_at": current_user.created_at.isoformat()
    }

@router.get("/", response_model=List[dict])
async def get_organization_users(
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Get all users in the current user's organization (Treasurer only).
    """
    statement = select(User).where(
        User.organization_id == current_user.organization_id
    ).offset(offset).limit(limit)
    
    users = session.exec(statement).all()
    
    return [
        {
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "contact_telephone": user.contact_telephone,
            "is_special_user": user.is_special_user,
            "special_user_type": user.special_user_type,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]

@router.get("/search")
async def search_users(
    q: str = Query(..., description="Search query (name or email)"),
    limit: int = Query(10, ge=1, le=100, description="Number of results"),
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Search for users within the organization (for Use Case 2.6 - Treasurer submits on behalf of member).
    """
    # Simple search - get all users and filter in Python
    statement = select(User).where(
        User.organization_id == current_user.organization_id
    ).limit(limit * 2)  # Get more to account for filtering
    
    all_users = session.exec(statement).all()
    
    # Filter users by search query
    users = []
    for user in all_users:
        if (user.full_name and q.lower() in user.full_name.lower()) or \
           (user.email and q.lower() in user.email.lower()):
            users.append(user)
            if len(users) >= limit:
                break
    
    return [
        {
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_special_user": user.is_special_user
        }
        for user in users
    ]

@router.post("/special", status_code=201)
async def create_special_user(
    type: SpecialUserType,
    name: Optional[str] = None,
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Create special user profiles (Anonymous Donor, Unknown User, or one-time donors) for Use Case 2.5.
    """
    # Generate appropriate name based on type
    if type == SpecialUserType.anonymous_donor:
        full_name = "Anonymous Donor"
    elif type == SpecialUserType.unknown_user:
        full_name = "Unknown User"
    elif type == SpecialUserType.one_time_donor:
        full_name = name or "One-Time Donor"
    else:
        raise HTTPException(status_code=400, detail="Invalid special user type")
    
    # Create special user
    special_user = User(
        full_name=full_name,
        email=None,  # Special users don't have emails
        hashed_password=None,  # Special users don't have passwords
        role=Role.member,
        is_special_user=True,
        special_user_type=type,
        organization_id=current_user.organization_id
    )
    
    session.add(special_user)
    session.commit()
    session.refresh(special_user)
    
    return {
        "id": str(special_user.id),
        "full_name": special_user.full_name,
        "is_special_user": special_user.is_special_user,
        "special_user_type": special_user.special_user_type,
        "organization_id": str(special_user.organization_id)
    }

@router.get("/{user_id}")
async def get_user_by_id(
    user_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get user by ID (must be in same organization).
    """
    statement = select(User).where(
        User.id == user_id,
        User.organization_id == current_user.organization_id
    )
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": str(user.id),
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "contact_telephone": user.contact_telephone,
        "is_special_user": user.is_special_user,
        "special_user_type": user.special_user_type,
        "created_at": user.created_at.isoformat()
    }

@router.put("/{user_id}/role")
async def update_user_role(
    user_id: str,
    new_role: str,
    current_user: User = Depends(require_treasurer_role),
    session: Session = Depends(get_session)
):
    """
    Update user role (Treasurer only).
    """
    if new_role not in ["member", "treasurer"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    statement = select(User).where(
        User.id == user_id,
        User.organization_id == current_user.organization_id
    )
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = Role(new_role)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {
        "message": "User role updated successfully",
        "user_id": str(user.id),
        "new_role": user.role
    }

@router.delete("/clear-all")
async def clear_all_users(session: AsyncSession = Depends(get_session)):
    """Clear all users from the database (for testing purposes)."""
    try:
        # Delete all users
        result = await session.exec(select(User))
        users = result.all()
        for user in users:
            await session.delete(user)
        await session.commit()
        return {"message": f"All {len(users)} users cleared successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear users: {str(e)}") 