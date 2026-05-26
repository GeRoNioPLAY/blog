from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate


async def create_post(db: AsyncSession, post_in: PostCreate) -> Post:
    db_post = Post(**post_in.model_dump())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)

    return db_post


async def get_posts(db: AsyncSession) -> Sequence[Post]:
    result = await db.scalars(select(Post))
    return result.all()


async def get_post_by_id(db: AsyncSession, post_id: int) -> Post | None:
    return await db.get(Post, post_id)
