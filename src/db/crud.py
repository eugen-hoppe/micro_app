from uuid import uuid4
from enum import Enum, auto

from fastapi import Depends, Request
from sqlalchemy.orm.session import Session as SessionLocal
from sqlalchemy import delete, select, update
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.orm import Session

from src.db.models import Base
from src.db.generic import Update


# CRUD
# ====
class Scope(Enum):
    READ = auto()
    WRITE = auto()


class DB:
    session: Session
    scope: Scope

    def __init__(self, session: Session, scope: Scope = Scope.READ):
        self.session = session
        self.scope = scope

    @staticmethod
    def allow(db: "DB", scope: Scope) -> None:
        if db.scope == scope:
            return None
        if scope != Scope.READ:
            raise PermissionError("Permission error: read-only")

    def create(self, payload: Base) -> Base:
        DB.allow(self, Scope.WRITE)
        if payload.alias is None:
            payload.alias = str(uuid4())
        self.session.add(payload)
        self.session.commit()
        self.session.refresh(payload)
        return payload

    def read(self, table: Base, id_or_alias: int | str) -> Base | None:
        def __select(table_, where_) -> ChunkedIteratorResult:
            return self.session.execute(select(table_).where(where_))

        DB.allow(self, Scope.READ)
        if isinstance(id_or_alias, int):
            return __select(table, table.id == id_or_alias).scalar_one_or_none()
        return __select(table, table.alias == id_or_alias).scalar_one_or_none()

    def update(
        self, table: Base, payload: Update, fetch: bool = False
    ) -> Base | None:
        def __update(table_, where_, values_) -> None:
            self.session.execute(update(table_).where(where_).values(**values_))
            self.session.commit()

        DB.allow(self, Scope.WRITE)
        payload_dict = payload.model_dump(exclude_unset=True, exclude_none=True)
        if payload.id is None:
            __update(table, table.alias == payload.alias, payload_dict)
        else:
            __update(table, table.id == payload.id, payload_dict)
        if fetch:
            return self.read(table, payload.id)

    def delete(self, table: Base, id_or_alias: int | str) -> None:
        def __delete(table_, where_) -> None:
            self.session.execute(delete(table_).where(where_))
            self.session.commit()

        DB.allow(self, Scope.WRITE)
        if isinstance(id_or_alias, int):
            return __delete(table, table.id == id_or_alias)
        return __delete(table, table.alias == id_or_alias)


# Dependencies
# ============
async def get_db(request: Request):
    session: SessionLocal = getattr(request.state, "db")
    try:
        yield session
    finally:
        session.close()


async def write(session: SessionLocal = Depends(get_db)) -> DB:
    return DB(session, scope=Scope.WRITE)


async def read(session: SessionLocal = Depends(get_db)) -> DB:
    return DB(session)
