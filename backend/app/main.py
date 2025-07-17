from fastapi import FastAPI
from app.core.config import settings

def create_app() -> FastAPI:
    """
    Creates the FastAPI application.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Placeholder for API routers
    # from app.api.v1 import api_router
    # app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the GoodStewards API"}

    return app

app = create_app()
