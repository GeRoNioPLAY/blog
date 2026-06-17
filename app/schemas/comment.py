from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class CommentRead(BaseModel):
    id: int
    text: str
    created_at: datetime
    post_id: int

    model_config = ConfigDict(from_attributes=True)
