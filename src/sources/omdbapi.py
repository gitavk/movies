import asyncio
import datetime as dt
import json
from logging import getLogger

import httpx
from fastapi import HTTPException, status

from src.config import RAW_PATH, settings
from src.schemas.movie import MovieSchema

LOGGER = getLogger(__file__)


async def process_api_response(client, imd_id):
    with RAW_PATH.open("a") as resp_store:
        url = settings.API_URL_ID.format(**{"API_KEY": settings.API_KEY, "imd_id": imd_id})
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


def single_request(title: str) -> MovieSchema:
    with httpx.Client(timeout=10.0) as client:
        url = settings.API_URL_TITLE.format(**{"API_KEY": settings.API_KEY, "title": title})
        mdata = client.get(url).json()
    imdbid = mdata.pop("imdbID", None)
    if not imdbid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return MovieSchema(
        imdbid=imdbid,
        data=mdata,
        created_at=dt.datetime.utcnow(),
    )
