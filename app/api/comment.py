from fastapi import APIRouter, HTTPException

from app.core.deps import SessionDep
from app.crud import comment as crud_comment
from app.crud import post as crud_post
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter()


@router.post("/{post_id}/comments", response_model=CommentRead, status_code=201)
async def create_comment(
    post_id: int, comment_in: CommentCreate, db: SessionDep
) -> Comment:
    result = await crud_post.get_post_by_id(post_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return await crud_comment.create_comment(comment_in, post_id, db)
