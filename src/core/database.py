from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.core.conf import settings


class Base(DeclarativeBase):
    """Single declarative base all models inherit from."""


engine = create_async_engine(settings.DATABASE_URL, echo=settings.SQL_ECHO)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
