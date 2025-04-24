from sqlalchemy import JSON, Boolean, Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.properties import MappedColumn
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import UniqueConstraint

from src.db.relations import Many, One


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


# Database Schema
# ===============
membership = Table(
    "membership",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("subscription_id", ForeignKey("subscription.id")),
    Column("user_id", ForeignKey("user.id")),
    UniqueConstraint(
        "subscription_id", "user_id", name="uq_membership_subscription_user"
    ),
)


class Subscription(Base):
    owner: Mapped["User"] = One.to_one().PLAN.entity()
    accounts: Mapped[list["Account"]] = Many.to_one().SUBSCRIPTION.entity()
    members: Mapped[list["User"]] = Many.to_many().MEMBERSHIPS.over(membership)


class User(Base):
    alias = Column(String(64), unique=True, index=True)
    subscription_id: Mapped[int] = Base.foreign_key(Subscription.id)

    plan: Mapped[Subscription] = One.to_one().OWNER.by(subscription_id)
    memberships: Mapped[list[Subscription]] = Many.to_many().MEMBERS.over(membership)


class Account(Base):
    active = Column(Boolean, default=False)
    subscription_id: Mapped[int] = Base.foreign_key(Subscription.id)

    subscription: Mapped[Subscription] = One.to_many().ACCOUNTS.by(subscription_id)
