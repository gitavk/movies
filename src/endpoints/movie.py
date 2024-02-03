from typing import Any

from fastapi import APIRouter, Depends, status

import src.crud.movie as crud
from src.auth.user import get_current_user_is_admin
from src.endpoints.deps import SessionDep
from src.schemas.movie import MovieRequestSchema, MovieSchema

router = APIRouter()


@router.get("/", response_model=list[MovieSchema])
def read_movies(session: SessionDep, page: int = 1, per_page: int = 10) -> Any:
    return crud.get_list(session, page, per_page)


@router.get("/search/{title}", response_model=MovieSchema)
def search_movie(session: SessionDep, title: str) -> Any:
    return crud.get_by_title(session, title)


@router.get("/{imdbid}", response_model=MovieSchema)
def get_movie(session: SessionDep, imdbid: str) -> Any:
    return crud.get_one(session, imdbid)


@router.post("/", response_model=MovieSchema, status_code=status.HTTP_201_CREATED)
def upload(session: SessionDep, request: MovieRequestSchema) -> Any:
    return crud.upload(session, request)


@router.delete("/{imdbid}", dependencies=[Depends(get_current_user_is_admin)], status_code=status.HTTP_204_NO_CONTENT)
def delete(session: SessionDep, imdbid: str):
    crud.delete(session, imdbid)
