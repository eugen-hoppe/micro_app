from __future__ import annotations

from fastapi import APIRouter

from src.apps.user.crud import get_user
from src.apps.user.models import UserAPI
from src.db.database import DB


user_api = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@user_api.get("/{id_or_alias}", response_model=UserAPI)
async def api_get_user(id_or_alias: str, db: DB = DB.dependency()):
    return await get_user(id_or_alias, db=db)
