import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "GoodStewards API"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg_async://postgres:postgres@localhost/goodstewards")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_in_env")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # BAML
    BAML_CLIENT_MODE: str = "http"
    BAML_CLIENT_URL: str = os.getenv("BAML_CLIENT_URL", "http://localhost:2022")

    # Cloudflare R2
    R2_ACCESS_KEY_ID: str = os.getenv("R2_ACCESS_KEY_ID", "")
    R2_SECRET_ACCESS_KEY: str = os.getenv("R2_SECRET_ACCESS_KEY", "")
    R2_ENDPOINT_URL: str = os.getenv("R2_ENDPOINT_URL", "")
    R2_BUCKET_NAME: str = os.getenv("R2_BUCKET_NAME", "goodstewards-receipts")


    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
