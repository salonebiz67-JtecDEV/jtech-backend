"""
JTech AI — Brain

Handles communication between the JTech backend
and the Gemini API.
"""

from google import genai

from app.ai.context import build_conversation_context
from app.core.config import settings
from app.ai.prompts import SYSTEM_PROMPT


class JTechBrain:
    """Core AI engine for JTech."""

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate_response(
        self,
        user_message: str,
        conversation_messages: list[dict] | None = None,
    ) -> str:
        """
        Send a user message and optional conversation
        history to Gemini.
        """

        conversation_messages = (
            conversation_messages or []
        )

        conversation_context = (
            build_conversation_context(
                conversation_messages
            )
        )

        if conversation_context:
            prompt = (
                "CONVERSATION HISTORY:\n"
                f"{conversation_context}\n\n"
                "CURRENT USER MESSAGE:\n"
                f"{user_message}"
            )
        else:
            prompt = user_message

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
            },
        )

        if not response.text:
            return "I wasn't able to generate a response."

        return response.text


jtech_brain = JTechBrain()
