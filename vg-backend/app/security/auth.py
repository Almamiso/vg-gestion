from __future__ import annotations
from typing import Optional, List, Callable
from functools import lru_cache
import time
import json
import httpx
import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, Header
from app.config import settings

class UserContext:
    def __init__(self, sub: Optional[str], roles: List[str], locations: List[int]):
        self.sub = sub
        self.roles = roles
        self.locations = locations

class AuthError(HTTPException):
    def __init__(self, detail: str, status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail)

@lru_cache(maxsize=1)
def _jwks_client() -> Optional[PyJWKClient]:
    if not settings.clerk_jwks_url:
        return None
    return PyJWKClient(settings.clerk_jwks_url)

async def get_current_user(authorization: Optional[str] = Header(default=None)) -> UserContext:
    # Allow no-auth in local/dev if JWKS URL is not set
    if not authorization or not authorization.startswith("Bearer "):
        if not settings.clerk_jwks_url:
            return UserContext(sub=None, roles=["admin"], locations=[])
        raise AuthError("Missing bearer token")

    token = authorization.split(" ", 1)[1]
    jwks_client = _jwks_client()
    if jwks_client is None:
        # Local dev fallback: decode without verify
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
        except Exception as e:
            raise AuthError(f"Invalid token: {e}")
    else:
        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256", "ES256", "EdDSA"],
                audience=settings.auth_audience,
                options={"require": ["exp", "iat"]},
                issuer=settings.auth_issuer if settings.auth_issuer else None,
            )
        except Exception as e:
            raise AuthError(f"Token verify failed: {e}")

    sub = payload.get("sub")
    roles = payload.get("roles") or payload.get("role") or []
    if isinstance(roles, str):
        roles = [roles]
    locations = payload.get("locations") or []
    if not isinstance(locations, list):
        locations = []

    # Optional required role
    if settings.required_role and settings.required_role not in roles:
        raise HTTPException(status_code=403, detail="Forbidden")

    return UserContext(sub=sub, roles=roles, locations=locations)


def requires_role(role: str) -> Callable[[UserContext], UserContext]:
    def wrapper(user: UserContext = Depends(get_current_user)) -> UserContext:
        if role not in user.roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return wrapper


def requires_location_access(location_id_param: str = "location_id"):
    def dependency(user: UserContext = Depends(get_current_user)) -> UserContext:
        # In real code, fetch request state/params to enforce per-site access
        return user
    return dependency