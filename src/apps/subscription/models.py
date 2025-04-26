from __future__ import annotations

from src.db.generic import Data, Shape


class SubscriptionData(Data):
    year: int
    category: str = "Standard Plan"


class SubscriptionAPI(Shape):
    members: list[Shape] | None = None

    class Config:
        from_attributes = True
