"""
JTech AI — Task Tool

Allows JTech to create persistent tasks for
the authenticated user.
"""

from typing import Any

from app.ai.tools import JTechTool, tool_registry
from app.tasks.service import task_service


async def create_task(
    user_id: str,
    access_token: str,
    title: str,
    description: str | None = None,
    priority: str = "normal",
    due_at: str | None = None,
) -> dict[str, Any]:
    """
    Create a persistent task for the authenticated user.
    """

    task = await task_service.create_task(
        user_id=user_id,
        access_token=access_token,
        title=title,
        description=description,
        priority=priority,
        due_at=due_at,
    )

    return {
        "status": "created",
        "task": task,
    }


task_tool = JTechTool(
    name="create_task",
    description=(
        "Create a persistent task for the authenticated "
        "user. Use this when the user asks JTech to add "
        "something to their task list."
    ),
    parameters={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Short title of the task.",
            },
            "description": {
                "type": "string",
                "description": (
                    "Optional detailed description."
                ),
            },
            "priority": {
                "type": "string",
                "enum": [
                    "low",
                    "normal",
                    "high",
                    "urgent",
                ],
                "description": "Task priority.",
            },
            "due_at": {
                "type": "string",
                "description": (
                    "Optional due date and time "
                    "in ISO 8601 format."
                ),
            },
        },
        "required": [
            "title",
        ],
    },
    handler=create_task,
)


# Register the tool with the central registry.
tool_registry.register(task_tool)
