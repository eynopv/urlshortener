from pydantic import ValidationError
import pytest

from .schemas import ShortUrl, NewShortUrl


def test_new_short_url_valid():
    short_url = NewShortUrl(destination="http://example.com")
    assert short_url.destination == "http://example.com"


def test_new_hosrt_url_invalid():
    with pytest.raises(ValidationError):
        NewShortUrl(destination="not-url")


def test_short_url_valid():
    short_url = ShortUrl(
        id=1, destination="http://example.com", code="valid-code", created_at=123, updated_at=321  # type: ignore
    )
    assert short_url.id == 1
    assert short_url.destination == "http://example.com"
    assert short_url.created_at == 123
    assert short_url.updated_at == 321


def test_short_url_invalid():
    with pytest.raises(ValidationError):
        ShortUrl(
            id="one", destination="http://example.com", code="valid-code", created_at=123, updated_at=321  # type: ignore
        )

    with pytest.raises(ValidationError):
        ShortUrl(
            id=1,
            destination="not-url",
            code="valid-code",
            created_at=123,
            updated_at=321,
        )
