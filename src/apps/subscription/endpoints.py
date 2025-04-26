from __future__ import annotations

from fastapi import APIRouter, status

from src.apps.subscription.models import SubscriptionAPI, SubscriptionData
from src.db.database import DB
from src.db.models import Subscription, User


subscription_api = APIRouter(
    prefix="/subscription",
    tags=["plan"],
    responses={404: {"description": "Not found"}},
)

@subscription_api.post(
    "/", response_model=SubscriptionAPI, status_code=status.HTTP_201_CREATED
)
async def create_subscription(
    payload: SubscriptionData,
    db: DB = DB.dependency(DB.w),
):
    async with db.tx():
        subscription = await db.create(Subscription(data=payload.to_dict()))

    return SubscriptionAPI(**subscription.__dict__)


@subscription_api.post(
    "/with-owner",
    response_model=SubscriptionAPI,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription_with_owner(
    payload: SubscriptionData,
    db: DB = DB.dependency(DB.w),
):
    async with db.tx():
        subscription = await db.create(Subscription(data=payload.to_dict()))
        await db.create(User(data={"name": "John"}, plan=subscription))
    return SubscriptionAPI(**subscription.__dict__)
