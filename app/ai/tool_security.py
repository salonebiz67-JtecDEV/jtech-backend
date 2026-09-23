"""
JTech AI — Tool Security

Defines security metadata for JTech tools.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolSecurity:
    """Security rules for a JTech tool."""

    requires_confirmation: bool = False
    requires_android_execution: bool = False
    requires_authentication: bool = True


TOOL_SECURITY: dict[str, ToolSecurity] = {
    "create_timer": ToolSecurity(
        requires_confirmation=False,
        requires_android_execution=True,
    ),

    "create_reminder": ToolSecurity(
        requires_confirmation=False,
        requires_android_execution=False,
    ),

    "create_task": ToolSecurity(
        requires_confirmation=False,
        requires_android_execution=False,
    ),
}


def get_tool_security(
    tool_name: str,
) -> ToolSecurity:
    """
    Return security metadata for a tool.

    Unknown tools default to the safest configuration.
    """

    return TOOL_SECURITY.get(
        tool_name,
        ToolSecurity(
            requires_confirmation=True,
            requires_android_execution=True,
            requires_authentication=True,
        ),
    )
