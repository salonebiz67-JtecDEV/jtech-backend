"""
JTech AI Backend
"""

from fastapi import FastAPI

from app.core.config import settings
from app.core.identity import AI_NAME, AI_FULL_NAME, DEVELOPER_NAME


app = FastAPI(
    title=AI_FULL_NAME,
    version=settings.app_version,
    description="Backend for JTech AI.",
)


@app.get("/")
async def root():
    return {
        "name": AI_NAME,
        "full_name": AI_FULL_NAME,
        "developer": DEVELOPER_NAME,
        "version": settings.app_version,
        "status": "online",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "assistant": AI_NAME,
    }
