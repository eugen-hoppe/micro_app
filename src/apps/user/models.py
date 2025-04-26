from __future__ import annotations

from typing import List, Optional

from src.db.generic import Data, Shape


from src.apps.subscription.models import SubscriptionAPI


class UserData(Data):
    name: str


class UserAPI(Shape):
    plan: Optional[SubscriptionAPI] = None
    memberships: Optional[List[SubscriptionAPI]] = None

    class Config:
        from_attributes = True
