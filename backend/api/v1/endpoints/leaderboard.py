from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ....core.database import get_db
from ....services.user_service import UserService

router = APIRouter()

@router.get("/")
async def get_leaderboard(page: int = Query(1, ge=1), country: Optional[str] = Query(None), db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_leaderboard(page=page, country=country)
