from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, description="Простой Blog API", version="0.1.2"
)

app.include_router(api_router)
