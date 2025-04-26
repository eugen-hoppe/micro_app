from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from src.db.generic import Base


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
    owner: Mapped["User"] = relationship(
        back_populates="plan", uselist=False, cascade="all, delete-orphan"
    )
    accounts: Mapped[list["Account"]] = relationship(
        back_populates="subscription", cascade="all, delete-orphan"
    )
    members: Mapped[list["User"]] = relationship(
        secondary=membership, back_populates="memberships"
    )


class User(Base):
    subscription_id: Mapped[int | None] = mapped_column(
        ForeignKey("subscription.id", ondelete="CASCADE")
    )
    plan: Mapped["Subscription"] = relationship(
        back_populates="owner", uselist=False
    )
    memberships: Mapped[list["Subscription"]] = relationship(
        secondary=membership, back_populates="members"
    )


class Account(Base):
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscription.id", ondelete="CASCADE")
    )
    subscription: Mapped["Subscription"] = relationship(
        back_populates="accounts"
    )
