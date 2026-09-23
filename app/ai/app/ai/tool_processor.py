"""
JTech AI — Tool Call Processor

Processes requested JTech tools through security
checks and the controlled tool executor.
"""

from typing import Any

from app.ai.tool_calls import (
    JTechToolCall,
    JTechToolResult,
)
from app.ai.tool_executor import (
    ToolExecutionError,
    tool_executor,
)
from app.ai.tool_security import (
    get_tool_security,
)


class ToolProcessor:
    """Processes and executes JTech tool calls."""

    async def process(
        self,
        tool_call: JTechToolCall,
        user_id: str,
        access_token: str,
    ) -> JTechToolResult:
        """
        Process a single tool call.

        Authentication information is injected by the
        backend rather than being trusted from Gemini.
        """

        security = get_tool_security(
            tool_call.name
        )

        if security.requires_authentication:
            if not user_id or not access_token:
                return JTechToolResult(
                    name=tool_call.name,
                    success=False,
                    error="Authentication required.",
                )

        arguments: dict[str, Any] = {
            **tool_call.arguments,
        }

        # Never allow Gemini to choose the authenticated
        # user's identity.
        arguments["user_id"] = user_id
        arguments["access_token"] = access_token

        try:
            result = await tool_executor.execute(
                tool_name=tool_call.name,
                arguments=arguments,
            )

            return JTechToolResult(
                name=tool_call.name,
                success=True,
                result=result,
            )

        except ToolExecutionError as exc:
            return JTechToolResult(
                name=tool_call.name,
                success=False,
                error=str(exc),
            )

    def requires_confirmation(
        self,
        tool_name: str,
    ) -> bool:
        """Check whether a tool requires user confirmation."""

        return get_tool_security(
            tool_name
        ).requires_confirmation

    def requires_android_execution(
        self,
        tool_name: str,
    ) -> bool:
        """Check whether Android must execute the action."""

        return get_tool_security(
            tool_name
        ).requires_android_execution


tool_processor = ToolProcessor()
