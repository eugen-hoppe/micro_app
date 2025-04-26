from __future__ import annotations
from typing import Any, List, TYPE_CHECKING

from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.association import membership

if TYPE_CHECKING:
    from .user import User

class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alias: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    year: Mapped[int]
    category: Mapped[str] = mapped_column(String, default="Standard Plan")
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    owner: Mapped["User"] = relationship(back_populates="plan", uselist=False)
    members: Mapped[List["User"]] = relationship(
        secondary=membership, back_populates="memberships"
    )
