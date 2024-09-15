"""This module contains FastAPI dependencies"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides database session

    :return: Session instance generator
    """
    async with SessionLocal() as session:
        yield session
