from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ....core.database import get_db
from ....models.announcement import Announcement

router = APIRouter()

@router.get("/")
async def get_announcements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Announcement).order_by(Announcement.is_pinned.desc(), Announcement.created_at.desc()).limit(20))
    return [{"id": a.id, "title": a.title, "content": a.content, "is_pinned": a.is_pinned, "created_at": a.created_at} for a in result.scalars().all()]
