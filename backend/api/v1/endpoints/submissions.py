from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ....core.database import get_db
from ....core.deps import get_current_user
from ....models.user import User
from ....models.submission import Submission
from ....models.challenge import Challenge

router = APIRouter()

@router.get("/my")
async def my_submissions(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db), page: int = Query(1, ge=1)):
    query = select(Submission, Challenge.title).join(Challenge).where(Submission.user_id == current_user.id).order_by(Submission.submitted_at.desc())
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    results = (await db.execute(query.offset((page - 1) * 20).limit(20))).all()
    return {"submissions": [{"id": s.Submission.id, "challenge_title": s.title, "status": s.Submission.status.value, "points_earned": s.Submission.points_earned, "attempt_number": s.Submission.attempt_number, "submitted_at": s.Submission.submitted_at} for s in results], "total": total, "page": page}
