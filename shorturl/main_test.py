from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200


def test_create_shorturl():
    response = client.post("/", data={"destination": "http://example.com"})
    assert response.status_code == 200


def test_create_shorturl_invalid():
    response = client.post("/", data={"destination": "example.com"})
    assert response.status_code == 403


def test_get_shorturl_not_found():
    response = client.get("/non-existant")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


def test_get_shorturl():
    response = client.get("/existant", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["Location"] == "http://example.com/redirected"
