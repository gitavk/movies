from typing import Any

from fastapi import APIRouter

import src.crud.movie as crud
from src.endpoints.deps import SessionDep
from src.schemas.movie import MovieSchema

router = APIRouter()


@router.get("/", response_model=list[MovieSchema])
def read_movies(session: SessionDep, page: int = 1, per_page: int = 10) -> Any:
    return crud.get_list(session, page, per_page)
