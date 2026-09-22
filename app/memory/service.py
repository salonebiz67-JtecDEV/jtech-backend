"""
JTech AI — Memory Service

Handles long-term memory operations.
"""

from typing import Any

from app.core.config import settings


class MemoryService:
    """Handles JTech long-term memory."""

    def __init__(self) -> None:
        self.supabase_url = settings.supabase_url
        self.supabase_key = settings.supabase_key

    async def save_memory(
        self,
        user_id: str,
        category: str,
        content: str,
        importance: int = 5,
    ) -> dict[str, Any]:
        """
        Save a memory for a user.

        Supabase database integration will be added next.
        """

        return {
            "status": "pending",
            "user_id": user_id,
            "category": category,
            "content": content,
            "importance": importance,
        }

    async def get_memories(
        self,
        user_id: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve memories belonging to a user.

        Supabase database integration will be added next.
        """

        return []


memory_service = MemoryService()
