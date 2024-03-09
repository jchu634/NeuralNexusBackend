from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from library.database import models
from library.config import Settings

SQLALCHEMY_DATABASE_URL = "'sqlite+aiosqlite:///name.db'"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
Base: DeclarativeMeta = declarative_base()

if Settings.MEMORY_DATABASE:
    engine = create_async_engine(
        "sqlite+pysqlite:///:memory:", echo=True, future=True
    )
else:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):

    yield SQLAlchemyAccessTokenDatabase(session, models.AccessToken)
