import datetime as dt
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Text

from .engine import Base


class Movie(Base):
    __tablename__ = "movies"
    imdbid: Mapped[str] = mapped_column(Text, primary_key=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)
