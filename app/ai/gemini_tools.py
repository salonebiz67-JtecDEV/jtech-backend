"""
JTech AI — Gemini Tools

Builds Gemini-compatible tool declarations from
the JTech tool registry.
"""

from typing import Any

from app.ai.tools import tool_registry


def build_gemini_tool_declarations() -> list[dict[str, Any]]:
    """
    Build function declarations for Gemini.

    Only tools explicitly registered in the JTech
    tool registry are exposed to Gemini.
    """

    declarations: list[dict[str, Any]] = []

    for tool in tool_registry.list_tools():
        declarations.append(
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            }
        )

    return declarations
