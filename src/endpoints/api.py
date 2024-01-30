from fastapi import APIRouter

from .movie import router as movie_router

api_router = APIRouter()
api_router.include_router(movie_router)

__all__ = ["api_router"]
