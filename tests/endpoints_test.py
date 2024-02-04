import pytest


def test_list_default(fake_crud, test_client):
    resp = test_client.get("/")
    data = resp.json()
    assert resp.status_code == 200
    assert len(data) == 10
    titles = [x["data"]["Title"] for x in data]
    assert titles == sorted(titles)


@pytest.mark.parametrize(
    "page, per_page, expected",
    (
        (1, 5, 5),
        (100, 10, 0),
        (5, 6, 1),
        (1, 100, 25),
    ),
)
def test_list_page(fake_crud, test_client, page, per_page, expected):
    url = f"/?page={page}&per_page={per_page}"
    resp = test_client.get(url)
    data = resp.json()
    assert len(data) == expected


@pytest.mark.parametrize(
    "imdbid, expected",
    (
        ("tt1305826", 200),
        ("not_exists", 404),
    ),
)
def test_get(fake_crud, test_client, imdbid, expected):
    url = f"/{imdbid}"
    resp = test_client.get(url)
    assert resp.status_code == expected


@pytest.mark.parametrize(
    "title, expected",
    (
        ("Adventure Time", 200),
        ("not_exists", 404),
    ),
)
def test_search(fake_crud, test_client, title, expected):
    url = f"/search/{title}"
    resp = test_client.get(url)
    assert resp.status_code == expected


def test_upload_404(fake_crud, test_client):
    resp = test_client.post("/", json={"title": "string never exists in this world"})
    assert resp.status_code == 404


def test_upload(fake_crud, test_client):
    resp = test_client.post("/", json={"title": "Green Book"})
    assert resp.status_code == 201
    resp = test_client.post("/", json={"title": "Green Book"})
    assert resp.status_code == 409
