from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from http import HTTPStatus

from pydantic import ValidationError

from .schemas import NewShortUrl
from .db import Client

templates = Jinja2Templates(directory="shorturl/templates")

app = FastAPI()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/")
async def create_short_url(request: Request, destination: str = Form("")):
    client = Client()
    try:
        data = NewShortUrl(destination=destination)
    except ValidationError as e:
        input_error = e.errors()[0].get("msg")
        return templates.TemplateResponse(
            request=request,
            name="partials/form.html",
            context={"destination": destination, "input_error": input_error},
            status_code=HTTPStatus.FORBIDDEN,
        )

    shorturl = client.create_shorturl(data)
    return templates.TemplateResponse(
        request=request,
        name="partials/url_created.html",
        context={"shorturl": shorturl},
    )


@app.get("/{code}")
async def get_shorturl(code: str):
    client = Client()
    shorturl = client.get_shorturl_by_code(code)
    if not shorturl:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Not found")
    return RedirectResponse(
        shorturl.destination, status_code=HTTPStatus.TEMPORARY_REDIRECT
    )
