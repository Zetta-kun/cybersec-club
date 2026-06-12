from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ....core.database import get_db
from ....core.deps import get_current_user
from ....models.user import User
from ....services.user_service import UserService

router = APIRouter()

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    profile = await UserService(db).get_user_profile(current_user.id)
    return profile if profile else {"id": str(current_user.id), "username": current_user.username, "rating": current_user.rating, "total_solved": current_user.total_solved, "total_points": current_user.total_points}
