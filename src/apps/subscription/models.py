from src.db.generic import Shape, Data


class SubscriptionData(Data):
    year: int
    category: str = "Standard Plan"


class SubscriptionAPI(Shape):
    members: list[Shape] | None = None

    class Config:
        from_attributes = True
