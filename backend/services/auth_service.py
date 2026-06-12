from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import security
from datetime import datetime

class AuthService:
    def __init__(self, db: AsyncSession): self.db = db
    
    async def register_user(self, data: UserCreate) -> User:
        existing = await self.db.scalar(select(User).where((User.username == data.username) | (User.email == data.email)))
        if existing: raise ValueError("İstifadəçi adı və ya email artıq mövcuddur")
        user = User(username=data.username, email=data.email, password_hash=security.get_password_hash(data.password), full_name=data.full_name)
        self.db.add(user); await self.db.flush(); await self.db.refresh(user)
        return user
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.db.scalar(select(User).where(User.username == username))
        if not user or not security.verify_password(password, user.password_hash): return None
        if user.is_banned: raise ValueError("Hesab banlanıb")
        user.last_login = datetime.utcnow(); await self.db.flush()
        return user
