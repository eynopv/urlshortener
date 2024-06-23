from typing import Annotated
from pydantic import BaseModel, AnyHttpUrl, BeforeValidator, TypeAdapter

HttpUrlAdapter = TypeAdapter(AnyHttpUrl)


class NewShortUrl(BaseModel):
    destination: Annotated[
        str,
        BeforeValidator(lambda x: str(HttpUrlAdapter.validate_python(x)).rstrip("/")),
    ]


class ShortUrl(NewShortUrl):
    id: int = 0
    code: str
    created_at: int
    updated_at: int
