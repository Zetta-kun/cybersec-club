from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from ..models.challenge import Challenge
from ..models.submission import Submission
from ..models.user import User
from ..core.security import security
from .rating_service import RatingSystem

class ChallengeService:
    def __init__(self, db: AsyncSession): self.db = db
    
    async def get_challenges(self, category=None, difficulty=None, search=None, page=1, per_page=20, user_id=None):
        query = select(Challenge).where(Challenge.is_draft == False, Challenge.is_hidden == False)
        if category: query = query.where(Challenge.category == category)
        if difficulty: query = query.where(Challenge.difficulty == difficulty)
        if search: query = query.where(Challenge.title.ilike(f"%{search}%"))
        query = query.order_by(Challenge.current_points.desc())
        total = await self.db.scalar(select(func.count()).select_from(query.subquery()))
        challenges = (await self.db.execute(query.offset((page - 1) * per_page).limit(per_page))).scalars().all()
        result = []
        for c in challenges:
            solved = False
            if user_id:
                s = await self.db.scalar(select(Submission).where(Submission.user_id == user_id, Submission.challenge_id == c.id, Submission.status == "correct"))
                solved = s is not None
            result.append({"id": c.id, "title": c.title, "slug": c.slug, "category": c.category.value, "difficulty": c.difficulty.value, "base_points": c.base_points, "current_points": c.current_points, "total_solves": c.total_solves, "total_attempts": c.total_attempts, "tags": c.tags, "is_solved": solved, "created_at": c.created_at})
        return {"challenges": result, "total": total, "page": page, "pages": (total + per_page - 1) // per_page}
    
    async def submit_flag(self, user_id: UUID, challenge_id: UUID, flag: str, ip: str) -> Dict:
        challenge = await self.db.get(Challenge, challenge_id)
        if not challenge: return {"status": "error", "message": "Challenge tapılmadı"}
        existing = await self.db.scalar(select(Submission).where(Submission.user_id == user_id, Submission.challenge_id == challenge_id, Submission.status == "correct"))
        if existing: return {"status": "already_solved", "message": "Artıq həll edilib"}
        is_correct = security.hash_flag(flag.strip()) == challenge.flag_hash
        attempts = (await self.db.scalar(select(func.count()).select_from(Submission).where(Submission.user_id == user_id, Submission.challenge_id == challenge_id))) or 0
        sub = Submission(user_id=user_id, challenge_id=challenge_id, submitted_flag=flag, status="correct" if is_correct else "incorrect", points_earned=challenge.current_points if is_correct else 0, attempt_number=attempts + 1, ip_address=ip)
        self.db.add(sub)
        if is_correct:
            is_fb = challenge.total_solves == 0
            challenge.total_attempts += 1; challenge.total_solves += 1
            if is_fb: challenge.first_blood_user_id = user_id; challenge.first_blood_at = datetime.utcnow(); sub.points_earned += int(challenge.current_points * 0.1)
            challenge.current_points = RatingSystem.calculate_dynamic_points(challenge.base_points, challenge.total_attempts, challenge.total_solves)
            user = await self.db.get(User, user_id)
            user.total_solved += 1; user.total_points += sub.points_earned
            today = datetime.utcnow().date()
            user.consecutive_days = user.consecutive_days + 1 if user.last_active_date == today - timedelta(days=1) else 1
            user.last_active_date = today
            await self.db.flush()
            return {"status": "correct", "message": "✅ Təbriklər!", "points_earned": sub.points_earned, "is_first_blood": is_fb, "attempts": attempts + 1}
        challenge.total_attempts += 1; await self.db.flush()
        return {"status": "incorrect", "message": "❌ Yanlış flag!", "attempts": attempts + 1}
