from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from ....core.database import get_db
from ....core.deps import require_admin
from ....models.user import User
from ....schemas.challenge import ChallengeCreate
from ....services.admin_service import AdminService

router = APIRouter()

@router.get("/dashboard")
async def dashboard(current_user: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    return await AdminService(db).get_dashboard_stats()

@router.get("/users")
async def get_users(search: Optional[str] = Query(None), page: int = Query(1, ge=1), current_user: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    return await AdminService(db).get_users(search=search, page=page)

@router.put("/users/{user_id}/ban")
async def toggle_ban(user_id: UUID, reason: Optional[str] = None, current_user: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    if current_user.id == user_id: raise HTTPException(400, "Özünüzü banlaya bilməzsiniz")
    return await AdminService(db).toggle_ban(user_id, reason)

@router.post("/challenges")
async def create_challenge(challenge: ChallengeCreate, current_user: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await AdminService(db).create_challenge(challenge.dict(), current_user.id)
    return {"message": "Challenge yaradıldı", "challenge_id": str(result.id)}
