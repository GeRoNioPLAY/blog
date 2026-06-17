from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.pages.post import router as pages_router

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME, description="Простой Blog API", version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix="/api")
app.include_router(pages_router, tags=["Pages"])
