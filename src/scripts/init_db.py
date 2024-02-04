import asyncio
import json
import random
from logging import getLogger

from src.config import IDS_SOURCE, RAW_PATH, settings
from src.db.engine import Base, SessionLocal, engine
from src.db.models import Movie
from src.sources.omdbapi import request_api

LOGGER = getLogger(__file__)


async def init_db():
    with RAW_PATH.open() as src, SessionLocal() as db_session:
        movies = []
        for movie in src.readlines():
            mdata = json.loads(movie)
            imdbid = mdata.pop("imdbID", None)
            if not imdbid:
                LOGGER.error(f"Not found pk {imdbid}")
                LOGGER.warning(json.dumps(mdata, indent=2))
            movies.append(Movie(imdbid=imdbid, data=mdata))
        db_session.add_all(movies)
        db_session.commit()


async def main():
    with SessionLocal() as db_session:
        if db_session.query(Movie).count() > 0:
            # Coner case: all records will be deleted.
            LOGGER.warning("DB was already processed. Stop here.")
            return 0
    with IDS_SOURCE.open() as ids_src:
        ids = [x.strip() for x in ids_src.readlines()]
        random.shuffle(ids)
        ids = ids[: settings.IDS_LIMIT]
        await request_api(ids)

    await init_db()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    total_load = asyncio.run(main())
    LOGGER.info(f"Total processed {total_load} ids.")
