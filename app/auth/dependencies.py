"""
JTech AI — Authentication Dependencies

Verifies Supabase access tokens and identifies
the authenticated JTech user.
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client, create_client

from app.core.config import settings


security = HTTPBearer()


supabase: Client = create_client(
    settings.supabase_url,
    settings.supabase_key,
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Verify the Supabase access token and return
    the authenticated user's information.
    """

    access_token = credentials.credentials

    try:
        response = supabase.auth.get_user(access_token)

        if not response or not response.user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token.",
            )

        user = response.user

        return {
            "id": str(user.id),
            "email": user.email,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed.",
        ) from exc
