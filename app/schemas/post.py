from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .comment import CommentRead


class PostCreate(BaseModel):
    title: str
    content: str


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostWithCommentsRead(PostRead):
    comments: list[CommentRead]
