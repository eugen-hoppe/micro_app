from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.database import get_session
from src.models.user import User

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")
htmx_init(templates=templates)

web_app = APIRouter(tags=["htmx"])


@web_app.get("/", response_class=HTMLResponse)
@htmx("index", "index")
async def root_page(request: Request):
    return {"greeting": "Hello World"}


@web_app.get("/users", response_class=HTMLResponse)
@htmx("users")
async def list_users(request: Request, db: AsyncSession = Depends(get_session)):
    users = (await db.execute(select(User.name))).scalars().all()
    return {"users": users}
