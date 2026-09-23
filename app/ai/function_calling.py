"""
JTech AI — Gemini Function Calling

Handles Gemini function-calling operations and routes
them through JTech's controlled tool system.
"""

from typing import Any

from google.genai import types

from app.ai.gemini_tools import build_gemini_tools
from app.ai.tool_calls import JTechToolCall
from app.ai.tool_processor import tool_processor


class FunctionCallingEngine:
    """Handles Gemini function-calling operations."""

    def get_tool_declarations(
        self,
    ) -> list[types.Tool]:
        """
        Return the Gemini-compatible JTech tools.
        """

        return build_gemini_tools()

    async def execute_tool_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        user_id: str,
        access_token: str,
    ) -> dict[str, Any]:
        """
        Execute a Gemini-requested tool through
        JTech's security and execution layers.
        """

        tool_call = JTechToolCall(
            name=tool_name,
            arguments=arguments,
        )

        result = await tool_processor.process(
            tool_call=tool_call,
            user_id=user_id,
            access_token=access_token,
        )

        if not result.success:
            return {
                "success": False,
                "tool": result.name,
                "error": result.error,
            }

        return {
            "success": True,
            "tool": result.name,
            "result": result.result,
        }

    def requires_confirmation(
        self,
        tool_name: str,
    ) -> bool:
        """
        Determine whether the requested tool requires
        user confirmation.
        """

        return tool_processor.requires_confirmation(
            tool_name
        )

    def requires_android_execution(
        self,
        tool_name: str,
    ) -> bool:
        """
        Determine whether Android must execute
        the requested action.
        """

        return tool_processor.requires_android_execution(
            tool_name
        )


function_calling_engine = FunctionCallingEngine()
