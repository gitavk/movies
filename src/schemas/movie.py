import datetime as dt
from typing import Any

from pydantic import BaseModel, ConfigDict


class MovieSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    imdbid: str
    created_at: dt.datetime
    data: dict[str, Any]
