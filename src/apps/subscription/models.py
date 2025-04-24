from src.db.generic import Shape, Data
from src.db.categories import SubsriptionType


class SubscriptionData(Data):
    year: int
    category: SubsriptionType = SubsriptionType.STANDARD.value


class SubscriptionAPI(Shape):
    members: list[Shape] | None = None

    class Config:
        from_attributes = True
