from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, Dict, Any
from uuid import UUID
from ..models.user import User
from ..models.submission import Submission
from .rating_service import RatingSystem

class UserService:
    def __init__(self, db: AsyncSession): self.db = db
    
    async def get_user_profile(self, user_id: UUID) -> Optional[Dict]:
        user = await self.db.get(User, user_id)
        if not user: return None
        rank, color = RatingSystem.get_rank(user.rating)
        return {
            "id": str(user.id), "username": user.username, "email": user.email,
            "full_name": user.full_name, "rating": user.rating,
            "max_rating": user.max_rating, "total_solved": user.total_solved,
            "total_points": user.total_points, "role": user.role.value,
            "rank": rank, "rank_color": color,
            "consecutive_days": user.consecutive_days or 0,
            "created_at": user.created_at
        }
    
    async def get_leaderboard(self, page: int = 1, per_page: int = 50, country: Optional[str] = None) -> Dict:
        query = select(User).where(User.is_banned == False).order_by(User.rating.desc())
        if country: query = query.where(User.country == country)
        total = await self.db.scalar(select(func.count()).select_from(query.subquery()))
        users = (await self.db.execute(query.offset((page - 1) * per_page).limit(per_page))).scalars().all()
        leaderboard = []
        for idx, user in enumerate(users, start=(page - 1) * per_page + 1):
            rank, color = RatingSystem.get_rank(user.rating)
            leaderboard.append({
                "rank": idx, "user_id": str(user.id), "username": user.username,
                "rating": user.rating, "max_rating": user.max_rating,
                "rank_name": rank, "rank_color": color,
                "total_solved": user.total_solved, "total_points": user.total_points,
                "country": user.country
            })
        return {"leaderboard": leaderboard, "total": total, "page": page, "pages": (total + per_page - 1) // per_page}
