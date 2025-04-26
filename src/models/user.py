from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.association import membership

if TYPE_CHECKING:          # only for IDEs & mypy
    from .subscription import Subscription

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alias: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str]

    subscription_id: Mapped[int | None] = mapped_column(
        ForeignKey("subscription.id", ondelete="CASCADE")
    )
    plan: Mapped["Subscription"] = relationship(back_populates="owner", uselist=False)
    memberships: Mapped[list["Subscription"]] = relationship(
        secondary=membership, back_populates="members"
    )
