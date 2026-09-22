"""
JTech AI — Conversation Context

Builds the conversation context that is sent
to the AI brain.
"""

from typing import Any


def build_conversation_context(
    messages: list[dict[str, Any]],
) -> str:
    """
    Convert stored conversation messages into
    a readable context for Gemini.
    """

    if not messages:
        return ""

    context_lines: list[str] = []

    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")

        if not content:
            continue

        if role == "user":
            speaker = "User"
        elif role == "assistant":
            speaker = "JTech"
        elif role == "system":
            speaker = "System"
        else:
            continue

        context_lines.append(
            f"{speaker}: {content}"
        )

    return "\n".join(context_lines)
