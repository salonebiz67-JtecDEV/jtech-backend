"""
JTech AI — Brain

Handles communication between the JTech backend
and the Gemini API.
"""

from google import genai

from app.core.config import settings
from app.ai.prompts import SYSTEM_PROMPT


class JTechBrain:
    """Core AI engine for JTech."""

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate_response(self, user_message: str) -> str:
        """
        Send a user message to Gemini and return
        JTech's response.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config={
                "system_instruction": SYSTEM_PROMPT,
            },
        )

        if not response.text:
            return "I wasn't able to generate a response."

        return response.text


jtech_brain = JTechBrain()
