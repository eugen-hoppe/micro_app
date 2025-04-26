from fastapi import APIRouter

from src.apps.user.models import UserData
from src.apps.user.crud import get_user
from src.db.crud import DB


user_api = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@user_api.get("/{id_or_alias}", response_model=UserData)
async def api_get_user(id_or_alias: str, db: DB = DB.dependency()):
    return UserData(**get_user(id_or_alias, db=db).data)
