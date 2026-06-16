from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.config import settings
from app.pages.post import router as pages_router

app = FastAPI(
    title=settings.PROJECT_NAME, description="Простой Blog API", version="0.2.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix="/api")
app.include_router(pages_router, tags=["Pages"])
