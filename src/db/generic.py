from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alias: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Data(BaseModel):
    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)


class Shape(BaseModel):
    id: int
    alias: str | None
    data: dict[str, Any]
    version: int

    class Config:
        from_attributes = True


class Update(BaseModel):
    id: int | None = None
    alias: str | None = None
    data: dict[str, Any] | None = None

    class Config:
        from_attributes = True
