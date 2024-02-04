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


def test_token(test_client):
    form_data = {"username": "admin", "password": "admin"}
    resp = test_client.post("/token", data=form_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert "access_token" in resp.json()
    assert resp.status_code == 200


def test_token_exc(test_client):
    form_data = {"username": "admin", "password": "wrong_pass"}
    resp = test_client.post("/token", data=form_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert resp.status_code == 401


def test_delete(fake_crud, test_client):
    form_data = {"username": "admin", "password": "admin"}
    resp = test_client.post("/token", data=form_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    headers = {"Authorization": f'Bearer {resp.json()["access_token"]}'}
    resp = test_client.delete("/tt1305826", headers=headers)
    assert resp.status_code == 204
    resp = test_client.delete("/tt1305826", headers=headers)
    assert resp.status_code == 404


def test_delete_exc(test_client):
    resp = test_client.delete("/tt1305826", headers={})
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}
    headers = {"Authorization": "Bearer randomstring"}
    resp = test_client.delete("/tt1305826", headers=headers)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}
