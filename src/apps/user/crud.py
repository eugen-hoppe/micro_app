from __future__ import annotations

from fastapi import HTTPException, status

from src.apps.user.models import UserAPI
from src.db.database import DB
from src.db.models import User


async def get_user(id_or_alias: str, db: DB = DB.dependency()) -> UserAPI:
    is_uuid = len(str(id_or_alias).split("-")) == 5
    key = id_or_alias if is_uuid else int(id_or_alias)

    user = await db.read(User, key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserAPI(**user.__dict__)
