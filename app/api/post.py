from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import post as crud_post
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead, PostWithCommentsRead

router = APIRouter(prefix="/posts", tags=["Posts"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=Sequence[PostRead])
async def get_posts(db: SessionDep) -> Sequence[Post]:
    return await crud_post.get_posts(db)


@router.post("/", response_model=PostRead, status_code=201)
async def create_post(db: SessionDep, post_in: PostCreate) -> Post:
    return await crud_post.create_post(db, post_in)


@router.get("/{post_id}", response_model=PostWithCommentsRead)
async def get_post_by_id(db: SessionDep, post_id: int) -> Post | None:
    result = await crud_post.get_post_with_comments(db, post_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return result
