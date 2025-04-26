from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

from src.core.database import Base

membership = Table(
    "membership",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("subscription_id", ForeignKey("subscription.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE")),
    UniqueConstraint("subscription_id", "user_id", name="uq_membership_subscription_user"),
)
