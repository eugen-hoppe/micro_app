from pydantic import BaseModel, Field
from src.db.generic import Data, Shape


class UserData(Data):
    name: str


class UserAPI(Shape):
    plan: Shape
    memberships: list[Shape]

    class Config:
        from_attributes = True
