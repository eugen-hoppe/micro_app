from enum import Enum

from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import Relationship
from sqlalchemy.orm.properties import MappedColumn
from sqlalchemy.sql.schema import Table

from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.ext.declarative import declared_attr


from src.db import models


# Database
# ========
class Base(DeclarativeBase):
    """Base class for all database models"""
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    alias = Column(String(64), unique=True, index=True, default=None)
    version = Column(Integer, default=1)
    data = Column(JSON, default=dict)

    @declared_attr
    def __tablename__(cls: "Base") -> str:
        return cls.__name__.lower()

    @staticmethod
    def foreign_key(column: Column, ondelete: str = "CASCADE") -> MappedColumn:
        """Create a foreign key constraint on the given column"""
        return mapped_column(ForeignKey(column, ondelete=ondelete))


# Payload
# =======
class Data(BaseModel):
    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)


# CRUD
# ====
class Shape(BaseModel):
    id: int
    alias: str
    data: dict
    version: int

    class Config:
        from_attributes = True

    @classmethod
    def from_db(cls, row):
        return cls(**row.__dict__)


class Update(BaseModel):
    id: int | None = None
    alias: str | None = None
    data: dict | None = None

    class Config:
        from_attributes = True


# Relations
# =========
class EntityRelation(Enum):
    @staticmethod
    def back_populates(to: "Enum", kwargs: dict = {}) -> Relationship:
        return relationship(**kwargs, back_populates=to.name.lower())

    def by(self, column: MappedColumn) -> Relationship:
        return EntityRelation.back_populates(self, kwargs={"foreign_keys": [column]})

    def entity(self) -> Relationship:
        return EntityRelation.back_populates(self)


class ManyGeneric(Enum):
    def over(self, table: Table) -> Relationship:
        return EntityRelation.back_populates(self, kwargs={"secondary": table})

    @classmethod
    def to_many(cls) -> "models.Many":
        return cls


class OneGeneric(Enum):
    def by(self, column: MappedColumn) -> Relationship:
        return EntityRelation.back_populates(
            self, kwargs={"foreign_keys": [column], "uselist": False}
        )

    def entity(self) -> Relationship:
        return EntityRelation.back_populates(self)

    @classmethod
    def to_one(cls) -> "models.One":
        return cls
