"""
JTech AI — Brain

Handles communication between the JTech backend
and the Gemini API, including controlled tool calls.
"""

from typing import Any

from google import genai
from google.genai import types

from app.ai.context import build_ai_context
from app.ai.gemini_tools import build_gemini_tools
from app.ai.tool_calls import JTechToolCall
from app.ai.tool_processor import tool_processor
from app.ai.prompts import SYSTEM_PROMPT
from app.core.config import settings


class JTechBrain:
    """Core AI engine for JTech."""

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def _build_prompt(
        self,
        user_message: str,
        conversation_messages: list[dict] | None,
        memory_context: str,
    ) -> str:
        """Build the prompt sent to Gemini."""

        ai_context = build_ai_context(
            conversation_messages=conversation_messages,
            memory_context=memory_context,
        )

        if ai_context:
            return (
                f"{ai_context}\n\n"
                "CURRENT USER MESSAGE:\n"
                f"{user_message}"
            )

        return user_message

    async def generate_response(
        self,
        user_message: str,
        conversation_messages: list[dict] | None = None,
        memory_context: str = "",
        user_id: str | None = None,
        access_token: str | None = None,
    ) -> str:
        """
        Generate a JTech response.

        Gemini may request registered tools. Tool execution
        is handled by JTech's own security and execution layers.
        """

        prompt = self._build_prompt(
            user_message=user_message,
            conversation_messages=conversation_messages,
            memory_context=memory_context,
        )

        tools = build_gemini_tools()

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=tools or None,
        )

        # Keep the complete Gemini conversation history for
        # the manual function-calling flow.
        contents: list[Any] = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=prompt
                    )
                ],
            )
        ]

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )

        # --------------------------------------------
        # NO TOOL CALL
        # --------------------------------------------

        if not response.function_calls:
            if not response.text:
                return (
                    "I wasn't able to generate a response."
                )

            return response.text

        # --------------------------------------------
        # TOOL CALLS REQUIRE AUTHENTICATED USER
        # --------------------------------------------

        if not user_id or not access_token:
            return (
                "I need an authenticated user before "
                "I can perform an action."
            )

        # --------------------------------------------
        # KEEP GEMINI'S TOOL-CALL RESPONSE
        # --------------------------------------------

        if not response.candidates:
            return (
                "JTech received an invalid response "
                "from the AI service."
            )

        model_content = response.candidates[0].content

        if model_content is None:
            return (
                "JTech received an incomplete tool request "
                "from the AI service."
            )

        contents.append(model_content)

        # --------------------------------------------
        # EXECUTE REQUESTED TOOLS
        # --------------------------------------------

        function_response_parts: list[types.Part] = []

        for function_call in response.function_calls:
            tool_name = function_call.name

            if not tool_name:
                continue

            arguments: dict[str, Any] = dict(
                function_call.args or {}
            )

            tool_call = JTechToolCall(
                name=tool_name,
                arguments=arguments,
            )

            result = await tool_processor.process(
                tool_call=tool_call,
                user_id=user_id,
                access_token=access_token,
            )

            if result.success:
                tool_result = {
                    "success": True,
                    "result": result.result,
                }
            else:
                tool_result = {
                    "success": False,
                    "error": result.error,
                }

            function_response_parts.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response=tool_result,
                    id=function_call.id,
                )
            )

        # --------------------------------------------
        # SEND TOOL RESULTS BACK TO GEMINI
        # --------------------------------------------

        if not function_response_parts:
            return (
                "JTech received an invalid tool request."
            )

        contents.append(
            types.Content(
                role="user",
                parts=function_response_parts,
            )
        )

        final_response = (
            self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config,
            )
        )

        if not final_response.text:
            return (
                "The action was processed, but I "
                "couldn't generate a final response."
            )

        return final_response.text


jtech_brain = JTechBrain()
