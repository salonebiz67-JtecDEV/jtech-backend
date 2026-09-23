"""
JTech AI — Tool Loader

Loads and registers all JTech tools.
"""

from app.ai import (
    tools_reminder,
    tools_task,
    tools_timer,
)


def load_tools() -> None:
    """
    Import all JTech tool modules so their tools
    are registered with the central registry.

    New tools should be imported here when they
    are added to the backend.
    """

    _ = (
        tools_timer,
        tools_reminder,
        tools_task,
    )
