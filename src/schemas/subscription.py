from typing import Any, Optional
from pydantic import BaseModel, Field


class SubscriptionCreate(BaseModel):
    year: int
    category: str = Field(default="Standard Plan")
    data: dict[str, Any] = Field(default_factory=dict)


class SubscriptionUpdate(BaseModel):
    year: Optional[int] = None
    category: Optional[str] = None
    data: Optional[dict[str, Any]] = None
