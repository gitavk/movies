import datetime as dt
import json
from copy import deepcopy
from pathlib import Path

import pytest
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient

from src.endpoints.deps import get_db
from src.main import app

BASE_PATH = Path(__file__)


def override_get_db():
    yield


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def test_client():
    return TestClient(app)


@pytest.fixture()
def _refresh_db():
    example_path = BASE_PATH.parent / "resources/omdbapi.json"
    with example_path.open() as in_data:
        for idx, line in enumerate(in_data.readlines()):
            data = json.loads(line)
            edata = deepcopy(data)
            item = {}
            item["imdbid"] = data.pop("imdbID")
            item["data"] = data
            item["created_at"] = dt.datetime.utcnow()
            if idx < 25:
                FakeMovieCrud.FakeDB[item["imdbid"]] = item
            else:
                FakeMovieCrud.ExtraData.append(edata)
        FakeMovieCrud.FakeDB = dict(sorted(FakeMovieCrud.FakeDB.items(), key=lambda item: item[1]["data"].get("Title")))
    yield
    FakeMovieCrud.FakeDB = {}
    FakeMovieCrud.ExtraData = []


class FakeMovieCrud:
    FakeDB = {}
    ExtraData = []

    @staticmethod
    def get_list(_, page: int, per_page: int):
        result = []
        skip = (page - 1) * per_page
        for idx, item in enumerate(FakeMovieCrud.FakeDB.values(), 1):
            if len(result) == per_page:
                break
            if idx > skip:
                result.append(item)
        return result

    @staticmethod
    def get_one(_, imdbid):
        item = FakeMovieCrud.FakeDB.get(imdbid)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        return item

    @staticmethod
    def get_by_title(_, title):
        for item in FakeMovieCrud.FakeDB.values():
            if item["data"]["Title"] == title:
                return item
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    @staticmethod
    def delete(_, imdbid):
        item = FakeMovieCrud.FakeDB.pop(imdbid, None)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    @staticmethod
    def upload(_, request):
        data = {}
        for eitem in FakeMovieCrud.ExtraData:
            if eitem["Title"] == request.title:
                data = deepcopy(eitem)
                break
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        if data["imdbID"] in FakeMovieCrud.FakeDB:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Movie already exists.")
        item = {}
        item["imdbid"] = data.pop("imdbID")
        item["data"] = data
        item["created_at"] = dt.datetime.utcnow()
        FakeMovieCrud.FakeDB[item["imdbid"]] = item
        return item


@pytest.fixture()
def fake_crud(monkeypatch, _refresh_db):
    monkeypatch.setattr("src.endpoints.movie.crud", FakeMovieCrud)
