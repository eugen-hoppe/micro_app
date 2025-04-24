from enum import Enum, auto

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import Relationship
from sqlalchemy.orm.properties import MappedColumn
from sqlalchemy.sql.schema import Table


class OneToMany(Enum):
    SUBSCRIPTION = auto()  # 1
    SUBSCRIPTIONS = auto()  # n
    USER = auto()  # 1
    USERS = auto()  # n
    ACCOUNT = auto()  # 1
    ACCOUNTS = auto()  # n

    @staticmethod
    def back_populates(to: "Enum", kwargs: dict = {}) -> Relationship:
        return relationship(**kwargs, back_populates=to.name.lower())

    def by(self, column: MappedColumn) -> Relationship:
        return OneToMany.back_populates(self, kwargs={"foreign_keys": [column]})

    def entity(self) -> Relationship:
        return OneToMany.back_populates(self)


class Many(Enum):
    MEMBERSHIPS = auto()  # n
    MEMBERS = auto()  # n

    def over(self, table: Table) -> Relationship:
        return OneToMany.back_populates(self, kwargs={"secondary": table})

    @staticmethod
    def to_many() -> "Many":
        return Many

    @staticmethod
    def to_one() -> OneToMany:
        return OneToMany


class One(Enum):
    PLAN = auto()  # 1
    OWNER = auto()  # 1

    def by(self, column: MappedColumn) -> Relationship:
        return OneToMany.back_populates(
            self, kwargs={"foreign_keys": [column], "uselist": False}
        )

    def entity(self) -> Relationship:
        return OneToMany.back_populates(self)

    @staticmethod
    def to_one() -> "One":
        return One

    @staticmethod
    def to_many() -> OneToMany:
        return OneToMany
