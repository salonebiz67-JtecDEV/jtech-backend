"""
JTech AI Backend
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.core.identity import AI_NAME, AI_FULL_NAME, DEVELOPER_NAME
from app.ai.brain import jtech_brain


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
async def chat(request: ChatRequest):
    """Send a message to JTech and receive an AI response."""

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
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="JTech was unable to process the request.",
        ) from exc
