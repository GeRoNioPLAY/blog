from fastapi import APIRouter

from app.api.comment import router as comment_router
from app.api.post import router as post_router

api_router = APIRouter()

api_router.include_router(comment_router)
api_router.include_router(post_router)
