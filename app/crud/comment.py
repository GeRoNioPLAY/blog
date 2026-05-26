from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.schemas.comment import CommentCreate


async def create_comment(db: AsyncSession, comment_in: CommentCreate, post_id: int) -> Comment:
    db_comment = Comment(**comment_in.model_dump(), post_id=post_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)

    return db_comment
