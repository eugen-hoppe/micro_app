from fastapi import APIRouter, Depends, status

from src.apps.subscription.models import SubscriptionAPI, SubscriptionData
from src.db.models import Subscription
from src.db.crud import DB, write


subscription_api = APIRouter(
    prefix="/subscription",
    responses={404: {"description": "Not found"}},
    tags=["plan"],
)


@subscription_api.post(
    "/create",
    response_model=SubscriptionAPI,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    subscription_data: SubscriptionData, db: DB = Depends(write)
):
    with db.tx():
        created_subscription = db.create(Subscription(data=subscription_data.to_dict()))
    return SubscriptionAPI.from_db(created_subscription)
