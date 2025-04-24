from enum import auto

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped
from sqlalchemy.schema import UniqueConstraint

from src.db.generic import EntityRelation, ManyGeneric, OneGeneric, Base


# Relation Definition
# ===================
class ToOne(EntityRelation):
    SUBSCRIPTION = auto()

class ToMany(EntityRelation):
    ACCOUNTS = auto()


class Many(ManyGeneric):
    MEMBERSHIPS = auto()
    MEMBERS = auto()

    @staticmethod
    def to_one() -> "ToOne":
        return ToOne


class One(OneGeneric):
    PLAN = auto()
    OWNER = auto()

    @staticmethod
    def to_many() -> "ToMany":
        return ToMany


# Many-To-Many Relations
# ======================
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


# Database Entities
# =================
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
