from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .comment import CommentRead


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostWithCommentsRead(PostRead):
    comments: list[CommentRead]
