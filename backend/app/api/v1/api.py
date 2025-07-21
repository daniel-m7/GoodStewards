from fastapi import APIRouter

from app.api.v1.endpoints import auth, receipts, users, organizations, forms, payments, feedback

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(receipts.router, prefix="/receipts", tags=["receipts"])
api_router.include_router(forms.router, prefix="/forms", tags=["forms"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"]) 