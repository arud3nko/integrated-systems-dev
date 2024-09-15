"""This module provides async session fabric"""


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app import get_postgres_conf

config = get_postgres_conf()

engine = create_async_engine(
    url=config.ASYNC_POSTGRES_URL,
)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
