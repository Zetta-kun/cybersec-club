from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from .database import get_db
from .security import security
from ..models.user import User
import time
from collections import defaultdict

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
rate_limit_store = defaultdict(list)

async def rate_limit(request: Request):
    client_ip = request.client.host
    current_time = time.time()
    rate_limit_store[client_ip] = [t for t in rate_limit_store[client_ip] if current_time - t < 60]
    if len(rate_limit_store[client_ip]) >= 60:
        raise HTTPException(status_code=429, detail="Too many requests")
    rate_limit_store[client_ip].append(current_time)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = security.verify_token(token)
    if not payload or payload.get("type") != "access":
        raise credentials_exception
    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception
    user = await db.get(User, UUID(user_id))
    if not user:
        raise credentials_exception
    if user.is_banned:
        raise HTTPException(status_code=403, detail="Account is banned")
    return user

async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.value not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def require_moderator(current_user: User = Depends(get_current_user)):
    if current_user.role.value not in ["moderator", "admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Moderator access required")
    return current_user
