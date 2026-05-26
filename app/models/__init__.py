from app.core.database import Base

from .comment import Comment
from .post import Post

__all__ = ("Base", "Comment", "Post")
