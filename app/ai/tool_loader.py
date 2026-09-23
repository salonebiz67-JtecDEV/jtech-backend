"""
JTech AI — Tool Loader

Loads and registers all JTech tools.
"""

from app.ai import tools_timer


def load_tools() -> None:
    """
    Import all JTech tool modules so their tools
    are registered with the central registry.

    The function is intentionally explicit so new tools
    can be added safely as the backend grows.
    """

    _ = tools_timer
