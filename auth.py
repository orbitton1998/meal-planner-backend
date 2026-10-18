from typing import Optional
from fastapi import Header, HTTPException
from supabase_client import supabase


def _verify_token(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization[len("Bearer "):].strip()
    try:
        response = supabase.auth.get_user(token)
    except Exception:
        return None
    return response.user if response else None


def get_current_user(authorization: Optional[str] = Header(None)):
    """Returns the authenticated user, or None for guest requests."""
    return _verify_token(authorization)


def require_user(authorization: Optional[str] = Header(None)):
    """Returns the authenticated user, or raises 401 if missing/invalid."""
    user = _verify_token(authorization)
    if user is None:
        raise HTTPException(status_code=401, detail="Missing or invalid authentication token")
    return user
