"""
JTech AI Backend
"""

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.ai.brain import jtech_brain
from app.api.conversations import (
    router as conversations_router,
)
from app.api.memory import router as memory_router
from app.api.settings import router as settings_router
from app.auth.dependencies import get_current_user
from app.conversation.service import conversation_service
from app.core.config import settings
from app.core.identity import (
    AI_FULL_NAME,
    AI_NAME,
    DEVELOPER_NAME,
)


app = FastAPI(
    title=AI_FULL_NAME,
    version=settings.app_version,
    description="Backend for JTech AI.",
)


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
    )

    conversation_id: str | None = None


class ChatResponse(BaseModel):
    assistant: str
    message: str
    user_id: str
    conversation_id: str


app.include_router(memory_router)

app.include_router(conversations_router)

app.include_router(settings_router)


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


@app.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Send a message to JTech as an authenticated user.

    The message is stored in the user's conversation,
    previous messages are loaded, and the complete
    conversation context is sent to Gemini.
    """

    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    user_id = current_user["id"]
    access_token = current_user["access_token"]

    try:
        # --------------------------------------------
        # CREATE OR USE CONVERSATION
        # --------------------------------------------

        conversation_id = request.conversation_id

        if conversation_id is None:
            conversation = (
                await conversation_service.create_conversation(
                    user_id=user_id,
                    access_token=access_token,
                )
            )

            conversation_id = conversation["id"]

        # --------------------------------------------
        # LOAD EXISTING CONVERSATION
        # --------------------------------------------

        previous_messages = (
            await conversation_service.get_messages(
                user_id=user_id,
                access_token=access_token,
                conversation_id=conversation_id,
            )
        )

        # --------------------------------------------
        # SAVE USER MESSAGE
        # --------------------------------------------

        await conversation_service.save_message(
            user_id=user_id,
            access_token=access_token,
            conversation_id=conversation_id,
            role="user",
            content=user_message,
        )

        # --------------------------------------------
        # GENERATE JTECH RESPONSE
        # --------------------------------------------

        response = jtech_brain.generate_response(
            user_message=user_message,
            conversation_messages=previous_messages,
        )

        # --------------------------------------------
        # SAVE JTECH RESPONSE
        # --------------------------------------------

        await conversation_service.save_message(
            user_id=user_id,
            access_token=access_token,
            conversation_id=conversation_id,
            role="assistant",
            content=response,
        )

        return ChatResponse(
            assistant=AI_NAME,
            message=response,
            user_id=user_id,
            conversation_id=conversation_id,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="JTech was unable to process the request.",
        ) from exc
