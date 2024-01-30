from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.engine import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
