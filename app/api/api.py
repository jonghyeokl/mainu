from fastapi import APIRouter

from app.api.user import router as user_router
from app.api.recommend import router as recommend_router
from app.api.select import router as select_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(recommend_router, prefix="/recommend", tags=["recommend"])
api_router.include_router(select_router, prefix="/select", tags=["select"])
