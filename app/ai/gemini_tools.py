"""
JTech AI — Gemini Tools

Builds Gemini-compatible tool declarations from
the JTech tool registry.
"""

from google.genai import types

from app.ai.tool_loader import load_tools
from app.ai.tools import tool_registry


def build_gemini_tools() -> list[types.Tool]:
    """
    Load all registered JTech tools and build
    Gemini-compatible tool declarations.
    """

    # Make sure all JTech tools are registered.
    load_tools()

    declarations = []

    for tool in tool_registry.list_tools():
        declarations.append(
            types.FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters=tool.parameters,
            )
        )

    if not declarations:
        return []

    return [
        types.Tool(
            function_declarations=declarations,
        )
    ]
