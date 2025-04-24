from fastapi import APIRouter, Depends, HTTPException, status

from src.apps.user.models import UserAPI, UserData
from src.db.models import User
from src.db.crud import DB, read


user_api = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


def get_user(id_or_alias: str, db: DB = Depends(read)):  # crud.py
    is_uuid = len(id_or_alias.split("-")) == 5
    user = db.read(User, id_or_alias if is_uuid else int(id_or_alias))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!",
        )
    return UserAPI.from_db(user)


@user_api.get("/{id_or_alias}", response_model=UserData)
async def api_get_user(id_or_alias: str, db: DB = Depends(read)):
    return UserData(**get_user(id_or_alias, db=db).data)
