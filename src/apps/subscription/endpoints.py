from uuid import uuid4

from fastapi import APIRouter, Depends
from src.apps.subscription.models import SubscriptionAPI, SubscriptionData
from src.db.models import Subscription
from src.db.categories import SubsriptionType
from src.db.crud import DB, write



subscription_api = APIRouter(
    prefix="/subscription",
    responses={404: {"description": "Not found"}},
    tags=["plan"],
)


@subscription_api.post(
    "/subscription/data",
    response_model=SubscriptionAPI,
    response_model_exclude_none=True,
)
async def create_subscription(
    subscription_data: SubscriptionData,
    db: DB = Depends(write),
):
    db_subscription = Subscription(
        alias=str(uuid4()),
        category=SubsriptionType.STANDARD,
        data=subscription_data.db(),
    )
    created_subscription = db.create(db_subscription)
    return SubscriptionAPI(**created_subscription.__dict__)

