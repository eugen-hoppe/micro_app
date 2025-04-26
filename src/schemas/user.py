from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    alias: Optional[str] = None  # let DB generate uuid if left blank
    subscription_id: Optional[int] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    subscription_id: Optional[int] = None
