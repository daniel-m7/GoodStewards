from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.models import FeedbackCategory, FeedbackStatus


class FeedbackCreate(BaseModel):
    category: FeedbackCategory
    description: str
    device_info: Optional[Dict[str, Any]] = None


class FeedbackResponse(BaseModel):
    id: UUID
    category: FeedbackCategory
    description: str
    submitted_at: datetime
    status: FeedbackStatus


class FeedbackList(BaseModel):
    id: UUID
    user_id: UUID
    category: FeedbackCategory
    description: str
    device_info: Optional[Dict[str, Any]] = None
    submitted_at: datetime
    status: FeedbackStatus 