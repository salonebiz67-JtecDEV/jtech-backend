"""
JTech AI — Reminder Tool

Allows JTech to request creation of a persistent reminder.
"""

from datetime import datetime
from typing import Any

from app.ai.tools import JTechTool, tool_registry
from app.reminders.service import reminder_service


async def create_reminder(
    user_id: str,
    access_token: str,
    title: str,
    remind_at: str,
    message: str | None = None,
    repeat_rule: str | None = None,
) -> dict[str, Any]:
    """
    Create a persistent reminder for the authenticated user.
    """

    title = title.strip()

    if not title:
        raise ValueError(
            "Reminder title cannot be empty."
        )

    remind_at = remind_at.strip()

    if not remind_at:
        raise ValueError(
            "Reminder date and time is required."
        )

    # Validate that the supplied value is a real ISO
    # 8601 datetime before sending it to the database.
    try:
        datetime.fromisoformat(
            remind_at.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError(
            "Reminder date and time must be valid "
            "ISO 8601 format."
        ) from exc

    if message is not None:
        message = message.strip() or None

    if repeat_rule is not None:
        repeat_rule = repeat_rule.strip() or None

    reminder = await reminder_service.create_reminder(
        user_id=user_id,
        access_token=access_token,
        title=title,
        remind_at=remind_at,
        message=message,
        repeat_rule=repeat_rule,
    )

    return {
        "status": "created",
        "reminder": reminder,
    }


reminder_tool = JTechTool(
    name="create_reminder",
    description=(
        "Create a reminder for the authenticated user. "
        "Use this when the user asks JTech to remind them "
        "about something at a specific date or time."
    ),
    parameters={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Short title of the reminder.",
            },
            "remind_at": {
                "type": "string",
                "description": (
                    "Reminder date and time in ISO 8601 format."
                ),
            },
            "message": {
                "type": "string",
                "description": (
                    "Optional additional reminder message."
                ),
            },
            "repeat_rule": {
                "type": "string",
                "description": (
                    "Optional repeat rule for the reminder."
                ),
            },
        },
        "required": [
            "title",
            "remind_at",
        ],
    },
    handler=create_reminder,
)


tool_registry.register(reminder_tool)
