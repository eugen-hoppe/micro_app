from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init

from src.apps.user.crud import get_user
from src.db.database import DB


logger = logging.getLogger(__name__)
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates"
)
web_app = APIRouter(tags=["htmx"])
htmx_init(templates=templates)


@web_app.get("/", response_class=HTMLResponse)
@htmx("index", "index")
async def root_page(request: Request):
    logger.debug("cookies: %s", request.cookies)
    return {"greeting": "Hello World"}


@web_app.get("/users", response_class=HTMLResponse)
@htmx("users")
async def list_users(request: Request, db: DB = DB.dependency()):
    target = request.headers.get("hx-target")
    logger.debug("hx-target: %s", target)
    limit = 1
    names: List[str] = []
    for uid in range(1, limit + 1):
        try:
            user = await get_user(str(uid), db)
            names.append(user.data.get("name", "404"))
        except Exception:
            names.append("404")
    return {"users": names}
