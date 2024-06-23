from .db import Client, generate_code
from .schemas import NewShortUrl


def test_client_has_correct_db():
    client = Client()
    assert client.db == "test.db"


def test_create_shorturl():
    client = Client()
    shorturl = client.create_shorturl(NewShortUrl(destination="http://example.com"))
    assert shorturl.id > 0
    assert shorturl.destination
    assert shorturl.created_at
    assert shorturl.updated_at


def test_get_shorturl():
    client = Client()
    shorturl = client.get_shorturl_by_code("existant")
    assert shorturl
    assert shorturl.id == 100


def test_get_shorturl_nonexistant():
    client = Client()
    shorturl = client.get_shorturl_by_code("non-existant")
    assert not shorturl


def test_generate_shorturl_length():
    url = generate_code()
    assert len(url) == 6

    url = generate_code(8)
    assert len(url) == 8


def test_generate_shorturl_unique():
    urls = [generate_code() for _ in range(10)]
    assert len(urls) == len(set(urls))
