from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from ..models.user import User, UserRole
from ..models.challenge import Challenge
from ..models.submission import Submission
from ..models.announcement import Announcement
from ..core.security import security

class AdminService:
    def __init__(self, db: AsyncSession): self.db = db
    
    async def get_dashboard_stats(self) -> Dict:
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        total_users = await self.db.scalar(select(func.count()).select_from(User))
        total_challenges = await self.db.scalar(select(func.count()).select_from(Challenge).where(Challenge.is_draft == False))
        total_submissions = await self.db.scalar(select(func.count()).select_from(Submission))
        correct = await self.db.scalar(select(func.count()).select_from(Submission).where(Submission.status == "correct"))
        weekly_solves = await self.db.scalar(select(func.count()).select_from(Submission).where(Submission.status == "correct", Submission.submitted_at >= week_ago))
        top_users = (await self.db.execute(select(User.username, User.rating, User.total_solved).where(User.is_banned == False).order_by(User.rating.desc()).limit(10))).all()
        return {
            "total_users": total_users, "total_challenges": total_challenges,
            "total_submissions": total_submissions, "correct_submissions": correct,
            "success_rate": round(correct / total_submissions * 100, 2) if total_submissions > 0 else 0,
            "weekly_solves": weekly_solves, "weekly_new_users": 0,
            "category_distribution": [], "difficulty_distribution": [],
            "top_users": [{"username": r.username, "rating": r.rating, "solved": r.total_solved} for r in top_users],
            "recent_activities": []
        }
    
    async def get_users(self, search: Optional[str] = None, role: Optional[str] = None, is_banned: Optional[bool] = None, page: int = 1, per_page: int = 20) -> Dict:
        query = select(User)
        if search: query = query.where(or_(User.username.ilike(f"%{search}%"), User.email.ilike(f"%{search}%")))
        if role: query = query.where(User.role == role)
        if is_banned is not None: query = query.where(User.is_banned == is_banned)
        query = query.order_by(User.rating.desc())
        total = await self.db.scalar(select(func.count()).select_from(query.subquery()))
        users = (await self.db.execute(query.offset((page - 1) * per_page).limit(per_page))).scalars().all()
        return {"users": users, "total": total, "page": page, "pages": (total + per_page - 1) // per_page}
    
    async def toggle_ban(self, user_id: UUID, reason: Optional[str] = None) -> Dict:
        user = await self.db.get(User, user_id)
        if not user: raise ValueError("İstifadəçi tapılmadı")
        user.is_banned = not user.is_banned
        user.ban_reason = reason if user.is_banned else None
        await self.db.flush()
        return {"user_id": str(user.id), "is_banned": user.is_banned, "message": f"İstifadəçi {'banlandı' if user.is_banned else 'banı açıldı'}"}
    
    async def change_role(self, user_id: UUID, new_role: str) -> Dict:
        if new_role not in [r.value for r in UserRole]: raise ValueError("Yanlış rol")
        user = await self.db.get(User, user_id)
        if not user: raise ValueError("İstifadəçi tapılmadı")
        old_role = user.role.value
        user.role = new_role
        await self.db.flush()
        return {"user_id": str(user.id), "old_role": old_role, "new_role": new_role}
    
    async def create_challenge(self, data: dict, author_id: UUID) -> Challenge:
        slug = data["title"].lower().replace(" ", "-")[:200]
        challenge = Challenge(
            title=data["title"], slug=slug, description=data["description"],
            category=data["category"], difficulty=data["difficulty"],
            base_points=data.get("base_points", 100),
            flag_hash=security.hash_flag(data["flag"]),
            hints=data.get("hints", []), files=data.get("files", []),
            tags=data.get("tags", []), author_id=author_id,
            is_draft=data.get("is_draft", False),
        )
        self.db.add(challenge)
        await self.db.flush()
        await self.db.refresh(challenge)
        return challenge
