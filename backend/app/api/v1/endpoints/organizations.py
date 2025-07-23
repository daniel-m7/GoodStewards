from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import get_current_active_user
from app.core.db import get_session
from app.models.models import Organization, User

router = APIRouter()

@router.get("/{organization_id}")
async def get_organization(
    organization_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get organization details (must belong to the organization).
    """
    # Verify user belongs to the organization
    if str(current_user.organization_id) != organization_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    statement = select(Organization).where(Organization.id == organization_id)
    organization = session.exec(statement).first()
    
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    return {
        "id": str(organization.id),
        "name": organization.name,
        "fein": organization.fein,
        "ntee_code": organization.ntee_code,
        "address": organization.address,
        "city": organization.city,
        "state": organization.state,
        "zip_code": organization.zip_code,
        "created_at": organization.created_at.isoformat()
    }

@router.put("/{organization_id}")
async def update_organization(
    organization_id: str,
    name: Optional[str] = None,
    fein: Optional[str] = None,
    ntee_code: Optional[str] = None,
    address: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Update organization details (Treasurer only).
    """
    # Verify user belongs to the organization and is treasurer
    if str(current_user.organization_id) != organization_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if current_user.role != "treasurer":
        raise HTTPException(status_code=403, detail="Treasurer role required")
    
    statement = select(Organization).where(Organization.id == organization_id)
    organization = session.exec(statement).first()
    
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Update fields if provided
    if name is not None:
        organization.name = name
    if fein is not None:
        organization.fein = fein
    if ntee_code is not None:
        organization.ntee_code = ntee_code
    if address is not None:
        organization.address = address
    if city is not None:
        organization.city = city
    if state is not None:
        organization.state = state
    if zip_code is not None:
        organization.zip_code = zip_code
    
    session.add(organization)
    session.commit()
    session.refresh(organization)
    
    return {
        "message": "Organization updated successfully",
        "organization": {
            "id": str(organization.id),
            "name": organization.name,
            "fein": organization.fein,
            "ntee_code": organization.ntee_code,
            "address": organization.address,
            "city": organization.city,
            "state": organization.state,
            "zip_code": organization.zip_code
        }
    }

@router.delete("/clear-all")
async def clear_all_organizations(session: AsyncSession = Depends(get_session)):
    """Clear all organizations from the database (for testing purposes)."""
    try:
        # Delete all organizations
        result = await session.exec(select(Organization))
        organizations = result.all()
        for organization in organizations:
            await session.delete(organization)
        await session.commit()
        return {"message": f"All {len(organizations)} organizations cleared successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear organizations: {str(e)}") 