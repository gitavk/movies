
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.models import Movie


def get_list(db: Session, page: int, per_page: int) -> list[Movie]:
    skip = (page - 1) * per_page
    db_obj = db.query(Movie).order_by(Movie.data["Title"]).offset(skip).limit(per_page)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_obj


def get_one(db: Session, imdbid: str) -> Movie:
    db_obj = db.get(Movie, imdbid)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_obj
