"""
JTech AI — Tool Executor

Safely resolves and executes registered JTech tools.
"""

from typing import Any

from app.ai.tools import tool_registry


class ToolExecutionError(Exception):
    """Raised when a JTech tool cannot be executed."""


class ToolExecutor:
    """Executes registered JTech tools."""

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a registered tool using validated arguments.
        """

        tool = tool_registry.get(tool_name)

        if tool is None:
            raise ToolExecutionError(
                f"Unknown JTech tool: {tool_name}"
            )

        arguments = arguments or {}

        try:
            result = await tool.handler(
                **arguments
            )

        except TypeError as exc:
            raise ToolExecutionError(
                f"Invalid arguments for tool "
                f"'{tool_name}'."
            ) from exc

        except ValueError as exc:
            raise ToolExecutionError(
                str(exc)
            ) from exc

        except Exception as exc:
            raise ToolExecutionError(
                f"Tool '{tool_name}' failed."
            ) from exc

        if not isinstance(result, dict):
            raise ToolExecutionError(
                f"Tool '{tool_name}' returned an invalid result."
            )

        return result


tool_executor = ToolExecutor()
