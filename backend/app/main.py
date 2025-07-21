import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.db import get_session
from app.models.models import SQLModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting GoodStewards API...")
    
    # Initialize database tables
    try:
        from sqlmodel import create_engine
        # Create sync engine for table creation
        sync_url = settings.DATABASE_URL.replace("postgresql+psycopg_async://", "postgresql://")
        sync_engine = create_engine(sync_url, echo=False)
        SQLModel.metadata.create_all(sync_engine)
        logger.info("Database tables initialized successfully")
        
        # Load test data in development environment
        environment = os.getenv("ENVIRONMENT", "production")
        if environment == "development":
            logger.info("Development environment detected - loading test data...")
            try:
                # Import and load test data
                from load_test_data import load_all_test_data
                load_all_test_data()
                logger.info("✅ Development: Test data loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load test data: {e}")
                logger.info("Continuing without test data...")
        else:
            logger.info("Production environment - skipping test data loading")
            
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {e}")
        # Don't raise in test environment - just log the error
        if "test" not in settings.DATABASE_URL.lower():
            logger.warning("Database initialization failed, but continuing in test mode")
    
    yield
    
    # Shutdown
    logger.info("Shutting down GoodStewards API...")


def create_app() -> FastAPI:
    """
    Creates the FastAPI application with proper configuration and middleware.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="GoodStewards API for non-profit tax refund management",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global exception handlers
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """
        Handle HTTP exceptions with proper logging and response format.
        """
        logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "error_code": f"HTTP_{exc.status_code}",
                "timestamp": "2024-01-01T00:00:00Z"  # TODO: Use actual timestamp
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        Handle validation errors with proper logging and response format.
        """
        logger.warning(f"Validation Error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "errors": exc.errors(),
                "error_code": "VALIDATION_ERROR",
                "timestamp": "2024-01-01T00:00:00Z"  # TODO: Use actual timestamp
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Handle unhandled exceptions with proper logging and generic response.
        """
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error_code": "INTERNAL_ERROR",
                "timestamp": "2024-01-01T00:00:00Z"  # TODO: Use actual timestamp
            }
        )

    # Include API routers
    try:
        from app.api.v1.api import api_router
        app.include_router(api_router, prefix=settings.API_V1_STR)
        logger.info("API routers included successfully")
    except ImportError as e:
        logger.error(f"Failed to import API routers: {e}")
        raise

    @app.get("/")
    async def read_root() -> dict:
        """
        Root endpoint providing API information.
        """
        return {
            "message": "Welcome to the GoodStewards API",
            "version": "1.0.0",
            "docs": f"{settings.API_V1_STR}/docs",
            "redoc": f"{settings.API_V1_STR}/redoc",
            "openapi": f"{settings.API_V1_STR}/openapi.json"
        }

    @app.get("/health")
    async def health_check() -> dict:
        """
        Health check endpoint for monitoring and load balancers.
        """
        try:
            # Test database connection
            async for session in get_session():
                # If we can get a session, the database is healthy
                break
            
            return {
                "status": "healthy",
                "database": "connected",
                "timestamp": "2024-01-01T00:00:00Z"  # TODO: Use actual timestamp
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise HTTPException(
                status_code=503,
                detail="Service unhealthy - database connection failed"
            )

    @app.get("/api/v1/")
    async def api_info() -> dict:
        """
        API information endpoint.
        """
        return {
            "api_version": "v1",
            "endpoints": {
                "auth": f"{settings.API_V1_STR}/auth",
                "users": f"{settings.API_V1_STR}/users",
                "organizations": f"{settings.API_V1_STR}/organizations",
                "receipts": f"{settings.API_V1_STR}/receipts",
                "forms": f"{settings.API_V1_STR}/forms",
                "payments": f"{settings.API_V1_STR}/payments",
                "feedback": f"{settings.API_V1_STR}/feedback"
            }
        }

    return app


# Create the application instance
app = create_app()
