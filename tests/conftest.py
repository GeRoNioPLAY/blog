from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
)

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.models import Base, Post

test_engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False)


@pytest.fixture(scope="session", autouse=True)
async def init_db() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def db_connection(_init_db: None) -> AsyncGenerator[AsyncConnection]:
    async with test_engine.connect() as connection:
        yield connection


@pytest.fixture(scope="function")
async def db_session(db_connection: AsyncConnection) -> AsyncGenerator[AsyncSession]:
    transaction = await db_connection.begin()

    async_session = AsyncSession(
        bind=db_connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield async_session
    finally:
        await transaction.rollback()
        await async_session.close()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    async def _override_get_db() -> AsyncGenerator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def test_post(db_session: AsyncSession) -> Post:
    post = Post(title="Существующий пост", content="Текст существующего поста")
    db_session.add(post)
    await db_session.commit()
    await db_session.refresh(post)
    return post
