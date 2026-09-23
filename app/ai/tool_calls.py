"""
JTech AI — Tool Call Contracts

Defines the structure used when Gemini requests
a JTech tool.
"""

from typing import Any

from pydantic import BaseModel, Field


class JTechToolCall(BaseModel):
    """A tool requested by the AI."""

    name: str = Field(
        ...,
        min_length=1,
    )

    arguments: dict[str, Any] = Field(
        default_factory=dict
    )


class JTechToolResult(BaseModel):
    """The result returned after executing a tool."""

    name: str = Field(
        ...,
        min_length=1,
    )

    success: bool

    result: dict[str, Any] = Field(
        default_factory=dict
    )

    error: str | None = None
