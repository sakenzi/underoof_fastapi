from sqlalchemy.ext.asyncio import (
    async_sessionmaker, 
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase, 
    sessionmaker,
)
from core.config import settings
from sqlalchemy import create_engine


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg2,  
    echo=False
)

SessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session_factory() as session:
        yield session