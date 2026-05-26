from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import comment as crud_comment
from app.crud import post as crud_post
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter(prefix="/posts", tags=["Posts"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.post("/{post_id}/comments", response_model=CommentRead, status_code=201)
async def create_comment(
    db: SessionDep, comment_in: CommentCreate, post_id: int
) -> Comment:
    result = await crud_post.get_post_by_id(db, post_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return await crud_comment.create_comment(db, comment_in, post_id)
