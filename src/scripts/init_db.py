import asyncio
import json
import os
import random
from logging import getLogger
from pathlib import Path

import httpx

from src.db.engine import Base, SessionLocal, engine
from src.db.models import Movie

LOGGER = getLogger(__file__)

IDS_SOURCE = Path("ids.txt")
RAW_PATH = Path("omdbapi.txt")
IDS_LIMIT = 30
API_KEY = os.environ["API_KEY"]
API_URL = "http://www.omdbapi.com/?i={imd_id}&pot=full&apikey={API_KEY}"


async def is_first_run():
    LOGGER.info(f"CHECK the {RAW_PATH} exists.")
    return not RAW_PATH.exists()


async def process_api_response(client, imd_id):
    with RAW_PATH.open("a") as resp_store:
        url = API_URL.format(**{"API_KEY": API_KEY, "imd_id": imd_id})
        try:
            resp = await client.get(url)
        except httpx.ConnectTimeout:
            LOGGER.error(f"Error on fetch data from: {url}.")
            return
        resp_store.write(json.dumps(resp.json()) + "\n")


async def request_api(ids) -> int:
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        for imd_id in ids:
            tasks.append(process_api_response(client, imd_id))
        LOGGER.info(f"Will process {len(tasks)} ids.")
        await asyncio.gather(*tasks)
    return len(tasks)


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
        ids = ids[:IDS_LIMIT]
        await request_api(ids)

    await init_db()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    total_load = asyncio.run(main())
    LOGGER.info(f"Total processed {total_load} ids.")
