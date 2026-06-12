from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
from ....core.database import get_db
from ....core.deps import get_current_user, rate_limit
from ....models.user import User
from ....models.challenge import Challenge
from ....models.submission import Submission
from ....schemas.challenge import FlagSubmission, FlagResponse
from ....services.challenge_service import ChallengeService

router = APIRouter()

@router.get("/")
async def list_challenges(
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    return await ChallengeService(db).get_challenges(
        category=category, difficulty=difficulty, search=search,
        page=page, user_id=current_user.id if current_user else None
    )

@router.get("/{challenge_id}")
async def get_challenge(
    challenge_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    challenge = await db.get(Challenge, challenge_id)
    if not challenge:
        raise HTTPException(404, "Challenge tapılmadı")
    is_solved = False
    if current_user:
        sub = await db.scalar(
            select(Submission).where(
                Submission.user_id == current_user.id,
                Submission.challenge_id == challenge_id,
                Submission.status == "correct"
            )
        )
        is_solved = sub is not None
    return {
        "id": challenge.id, "title": challenge.title, "slug": challenge.slug,
        "description": challenge.description,
        "category": challenge.category.value if hasattr(challenge.category, 'value') else challenge.category,
        "difficulty": challenge.difficulty.value if hasattr(challenge.difficulty, 'value') else challenge.difficulty,
        "base_points": challenge.base_points, "current_points": challenge.current_points,
        "total_solves": challenge.total_solves, "total_attempts": challenge.total_attempts,
        "tags": challenge.tags, "is_solved": is_solved, "created_at": challenge.created_at
    }

@router.post("/solve", response_model=FlagResponse)
async def submit_flag(
    sub: FlagSubmission,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(rate_limit)
):
    return await ChallengeService(db).submit_flag(
        current_user.id, sub.challenge_id, sub.flag, str(request.client.host)
    )
