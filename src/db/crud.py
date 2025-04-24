from uuid import uuid4
from enum import Enum, auto
from contextlib import contextmanager

from fastapi import Depends, Request, HTTPException
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

    def __init__(self, session: Session, scope: Scope = Scope.READ) -> None:
        self.session = session
        self.scope = scope

    @staticmethod
    def _check(db: "DB", needed: Scope) -> None:
        if needed is Scope.READ:
            return
        if db.scope is not Scope.WRITE:
            raise HTTPException(status_code=403, detail="Database scope is read-only")

    def create(self, payload: Base, flush: bool = True) -> Base:
        DB._check(self, Scope.WRITE)
        if payload.alias is None:
            payload.alias = str(uuid4())
        self.session.add(payload)
        if flush:
            self.session.flush()
        self.session.refresh(payload)
        return payload

    def read(self, table: type[Base], id_or_alias: int | str) -> Base | None:
        DB._check(self, Scope.READ)
        stmt = select(table).where(
            table.id == id_or_alias if isinstance(id_or_alias, int)
            else table.alias == id_or_alias
        )
        result: ChunkedIteratorResult = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def update(
        self,
        table: type[Base],
        payload: Update,
        *,
        fetch: bool = False,
        flush: bool = True,
    ) -> Base | None:
        DB._check(self, Scope.WRITE)
        values = payload.model_dump(exclude_unset=True, exclude_none=True)
        condition = (
            table.id == payload.id if payload.id is not None 
            else table.alias == payload.alias
        )
        self.session.execute(update(table).where(condition).values(**values))
        if flush:
            self.session.flush()
        if fetch:
            key = payload.id if payload.id is not None else payload.alias
            return self.read(table, key)

    def delete(
        self, table: type[Base], id_or_alias: int | str, *, flush: bool = True
    ) -> None:
        DB._check(self, Scope.WRITE)
        condition = (
            table.id == id_or_alias if isinstance(id_or_alias, int)
            else table.alias == id_or_alias
        )
        self.session.execute(delete(table).where(condition))
        if flush:
            self.session.flush()

    @contextmanager
    def tx(self):
        with self.session.begin():
            yield self


# Dependencies
# ============
async def get_db(request: Request):
    session: SessionLocal = getattr(request.state, "db")
    yield session


async def write(session: SessionLocal = Depends(get_db)) -> DB:
    return DB(session, scope=Scope.WRITE)


async def read(session: SessionLocal = Depends(get_db)) -> DB:
    return DB(session)
