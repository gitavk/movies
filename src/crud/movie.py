from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.db.models import Movie
from src.schemas.movie import MovieRequestSchema, MovieSchema
from src.sources.omdbapi import single_request


def get_list(db: Session, page: int, per_page: int) -> list[Movie]:
    skip = (page - 1) * per_page
    db_obj = db.query(Movie).order_by(Movie.data["Title"]).offset(skip).limit(per_page)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return db_obj


def get_one(db: Session, imdbid: str) -> Movie:
    db_obj = db.get(Movie, imdbid)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return db_obj


def get_by_title(db: Session, title: str) -> Movie:
    try:
        return db.query(Movie).filter(Movie.data["Title"].astext == title).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")


def upload(db: Session, request: MovieRequestSchema) -> Movie:
    omdb_data: MovieSchema = single_request(request.title)
    db_obj = db.get(Movie, omdb_data.imdbid)
    if db_obj:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Movie already exists.")
    mobj = Movie(imdbid=omdb_data.imdbid, data=omdb_data.data)
    db.add(mobj)
    db.commit()
    db.refresh(mobj)
    return mobj
