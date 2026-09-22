"""
JTech AI Backend
"""

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from app.ai.brain import jtech_brain
from app.api.memory import router as memory_router
from app.auth.dependencies import get_current_user
from app.core.config import settings
from app.core.identity import AI_FULL_NAME, AI_NAME, DEVELOPER_NAME


app = FastAPI(
    title=AI_FULL_NAME,
    version=settings.app_version,
    description="Backend for JTech AI.",
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    assistant: str
    message: str
    user_id: str


app.include_router(memory_router)


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


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    """Send a message to JTech as an authenticated user."""

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    try:
        response = jtech_brain.generate_response(
            request.message
        )

        return ChatResponse(
            assistant=AI_NAME,
            message=response,
            user_id=current_user["id"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="JTech was unable to process the request.",
        ) from exc
