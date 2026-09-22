"""
JTech AI — Memory Service

Handles long-term memory operations using Supabase.
"""

from typing import Any

from supabase import Client, create_client

from app.core.config import settings


class MemoryService:
    """Handles JTech long-term memory."""

    def __init__(self) -> None:
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key,
        )

    async def save_memory(
        self,
        user_id: str,
        category: str,
        content: str,
        importance: int = 5,
    ) -> dict[str, Any]:
        """Save a memory for the authenticated user."""

        if not content.strip():
            raise ValueError("Memory content cannot be empty.")

        if not 1 <= importance <= 10:
            raise ValueError(
                "Memory importance must be between 1 and 10."
            )

        response = (
            self.client
            .table("memories")
            .insert(
                {
                    "user_id": user_id,
                    "category": category,
                    "content": content.strip(),
                    "importance": importance,
                }
            )
            .execute()
        )

        if not response.data:
            raise RuntimeError("Failed to save memory.")

        return response.data[0]

    async def get_memories(
        self,
        user_id: str,
    ) -> list[dict[str, Any]]:
        """Retrieve memories for the authenticated user."""

        response = (
            self.client
            .table("memories")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return response.data or []


memory_service = MemoryService()
