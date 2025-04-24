from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.schema import UniqueConstraint

from src.db.generic import Base


# Many-To-Many
# ============
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


# DB Tables
# =========
class Subscription(Base):
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="plan",
        uselist=False,
        cascade="all, delete-orphan",
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        back_populates="subscription",
        cascade="all, delete-orphan",
    )
    members: Mapped[list["User"]] = relationship(
        "User",
        secondary=membership,
        back_populates="memberships",
    )


class User(Base):
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscription.id", ondelete="CASCADE")
    )
    plan: Mapped["Subscription"] = relationship(
        "Subscription",
        back_populates="owner",
        uselist=False,
    )
    memberships: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        secondary=membership,
        back_populates="members",
    )


class Account(Base):
    active = Column(Boolean, default=False)
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscription.id", ondelete="CASCADE")
    )
    subscription: Mapped["Subscription"] = relationship(
        "Subscription",
        back_populates="accounts",
    )