from src.db.generic import Shape, Data


class SubscriptionData(Data):
    created_at: str


class SubscriptionAPI(Shape):
    data: dict

    class Config:
        from_attributes = True
