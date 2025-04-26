from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init

from src.apps.user.crud import get_user
from src.db.crud import DB


web_app = APIRouter(tags=["htmx"])
htmx_init(templates=Jinja2Templates(directory=Path("src") / "templates"))


@web_app.get("/", response_class=HTMLResponse)
@htmx("index", "index")
async def root_page(request: Request):
    return {"greeting": "Hello World"}


@web_app.get("/users", response_class=HTMLResponse)
@htmx("users")
async def get_users(request: Request, db: DB = DB.dependency()):
    max = 1
    users = [get_user(str(id), db).data.get("name", "404") for id in range(1, max + 1)]
    return {"users": users}
