from fastapi import APIRouter

from .auth import router as auth_router
from .movie import router as movie_router

api_router = APIRouter()
api_router.include_router(movie_router)
api_router.include_router(auth_router)

__all__ = ["api_router"]
