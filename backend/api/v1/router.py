from fastapi import APIRouter
from .endpoints import auth, users, challenges, submissions, leaderboard, admin, announcements

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["Challenges"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["Submissions"])
api_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["Leaderboard"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(announcements.router, prefix="/announcements", tags=["Announcements"])
