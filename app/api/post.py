from collections.abc import Sequence

from fastapi import APIRouter, HTTPException

from app.core.deps import SessionDep
from app.crud import post as crud_post
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead, PostWithCommentsRead

router = APIRouter()


@router.get("/", response_model=Sequence[PostRead])
async def get_posts(db: SessionDep) -> Sequence[Post]:
    return await crud_post.get_posts(db)


@router.post("/", response_model=PostRead, status_code=201)
async def create_post(post_in: PostCreate, db: SessionDep) -> Post:
    return await crud_post.create_post(post_in, db)


@router.get("/{post_id}", response_model=PostWithCommentsRead)
async def get_post_by_id(post_id: int, db: SessionDep) -> Post:
    result = await crud_post.get_post_with_comments(post_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return result
