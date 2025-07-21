import json
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import get_current_active_user
from app.core.db import get_session
from app.models.models import User, Feedback, FeedbackStatus
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackList

router = APIRouter()


@router.post("/", response_model=FeedbackResponse, status_code=201)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Submit user feedback, bug reports, or feature requests.
    """
    try:
        # Convert device_info dict to JSON string
        device_info_json = json.dumps(feedback_data.device_info) if feedback_data.device_info else None
        
        feedback = Feedback(
            user_id=current_user.id,
            organization_id=current_user.organization_id,
            category=feedback_data.category,
            description=feedback_data.description,
            device_info=device_info_json,
            status=FeedbackStatus.submitted
        )
        
        session.add(feedback)
        await session.commit()
        await session.refresh(feedback)
        
        return FeedbackResponse(
            id=feedback.id,
            category=feedback.category,
            description=feedback.description,
            submitted_at=feedback.created_at,
            status=feedback.status
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to submit feedback")


@router.get("/", response_model=List[FeedbackList])
async def get_feedback(
    category: Optional[str] = Query(None, description="Filter by feedback category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieve feedback submissions (Treasurer only).
    """
    if current_user.role != "treasurer":
        raise HTTPException(status_code=403, detail="Only treasurers can view feedback")
    
    try:
        query = select(Feedback).where(Feedback.organization_id == current_user.organization_id)
        
        if category:
            query = query.where(Feedback.category == category)
        if status:
            query = query.where(Feedback.status == status)
        
        query = query.offset(offset).limit(limit)
        
        result = await session.exec(query)
        feedback_list = result.all()
        
        return [
            FeedbackList(
                id=feedback.id,
                user_id=feedback.user_id,
                category=feedback.category,
                description=feedback.description,
                device_info=json.loads(feedback.device_info) if feedback.device_info else None,
                submitted_at=feedback.created_at,
                status=feedback.status
            )
            for feedback in feedback_list
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve feedback") 