from fastapi import APIRouter, status

from src.apps.subscription.models import SubscriptionAPI, SubscriptionData
from src.db.models import Subscription, User
from src.db.crud import DB


subscription_api = APIRouter(
    prefix="/subscription",
    responses={404: {"description": "Not found"}},
    tags=["plan"],
)


@subscription_api.post(
    "/create",
    response_model=SubscriptionAPI,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    subscription_data: SubscriptionData,
    db: DB = DB.dependency(DB.w),
):
    with db.tx():
        created_subscription = db.create(Subscription(data=subscription_data.to_dict()))
    return SubscriptionAPI.from_db(created_subscription)


@subscription_api.post(
    "/create_with_user",
    response_model=SubscriptionAPI,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription_and_user(
    payload: SubscriptionData,
    db: DB = DB.dependency(DB.w),
):
    with db.tx():
        subscription = Subscription(data=payload.to_dict())
        owner = User(data={"name": "John"})
        owner.plan = db.create(subscription)
        owner.alias = owner.plan.alias
        owner.memberships.append(subscription)
        db.create(owner)
    return SubscriptionAPI.from_db(owner.plan)
