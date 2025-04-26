from __future__ import annotations

from contextlib import asynccontextmanager
from enum import Enum, auto
from typing import TypeVar
from uuid import uuid4

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.generic import Update
from src.db.models import Base
from src.db.dependencies import get_db


_T = TypeVar("_T", bound=Base)


class Scope(Enum):
    READ = auto()
    WRITE = auto()


class DB:
    r = Scope.READ
    w = Scope.WRITE

    def __init__(self, session: AsyncSession, scope: Scope = Scope.READ):
        self.session = session
        self.scope = scope

    @staticmethod
    async def _ensure_write(db: "DB") -> None:
        if db.scope is not Scope.WRITE:
            raise HTTPException(status_code=403, detail="Database scope is read‑only")

    @staticmethod
    def dependency(scope: Scope = Scope.READ):
        async def _dep(session: AsyncSession = Depends(get_db)) -> "DB":
            return DB(session, scope)
        return Depends(_dep)

    @asynccontextmanager
    async def tx(self):
        async with self.session.begin():
            yield self

    async def create(
        self, obj: _T, *, flush: bool = True
    ) -> _T:
        await DB._ensure_write(self)
        if obj.alias is None:
            obj.alias = str(uuid4())
        self.session.add(obj)
        if flush:
            await self.session.flush()
        await self.session.refresh(obj)
        return obj


    async def read(self, model: type[_T], id_or_alias: int | str) -> _T | None:
        stmt = select(model).where(
            (model.id == id_or_alias) if isinstance(id_or_alias, int)
            else (model.alias == id_or_alias)
        )
        result = await self.session.scalars(stmt)
        return result.first()


    async def update(self, model: type[_T], payload: Update, *, fetch: bool = False):
        await DB._ensure_write(self)
        values = payload.model_dump(exclude_unset=True, exclude_none=True)
        if not values:
            return None
        condition = (
            (model.id == payload.id) if payload.id else (model.alias == payload.alias)
        )
        await self.session.execute(update(model).where(condition).values(**values))
        await self.session.flush()
        if fetch:
            return await self.read(model, payload.id or payload.alias)
        return None

    async def delete(
        self, model: type[_T], key: int | str
    ) -> None:
        await DB._ensure_write(self)
        condition = (model.id == key) if isinstance(key, int) else (model.alias == key)
        await self.session.execute(delete(model).where(condition))
