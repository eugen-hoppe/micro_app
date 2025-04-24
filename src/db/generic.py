from pydantic import BaseModel
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.orm.properties import MappedColumn
from sqlalchemy.ext.declarative import declared_attr


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
    def from_db(cls, row: type[Base]):
        return cls.model_validate(row, from_attributes=True)


class Update(BaseModel):
    id: int | None = None
    alias: str | None = None
    data: dict | None = None

    class Config:
        from_attributes = True
