from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ....core.database import get_db
from ....core.security import security
from ....core.deps import rate_limit
from ....schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from ....services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db), _: None = Depends(rate_limit)):
    try:
        user = await AuthService(db).register_user(data)
        return user
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, request: Request, db: AsyncSession = Depends(get_db), _: None = Depends(rate_limit)):
    try:
        user = await AuthService(db).authenticate_user(data.username, data.password)
    except ValueError as e:
        raise HTTPException(403, str(e))
    if not user: raise HTTPException(401, "İstifadəçi adı və ya şifrə yanlışdır")
    access = security.create_access_token({"sub": str(user.id), "role": user.role.value})
    refresh = security.create_refresh_token({"sub": str(user.id)})
    return TokenResponse(access_token=access, refresh_token=refresh, expires_in=1800, user=UserResponse(id=user.id, username=user.username, email=user.email, full_name=user.full_name, rating=user.rating, max_rating=user.max_rating, total_solved=user.total_solved, total_points=user.total_points, role=user.role.value, is_verified=user.is_verified, created_at=user.created_at))
