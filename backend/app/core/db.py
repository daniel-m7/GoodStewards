from collections.abc import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

# Create an async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async database session.
    """
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
