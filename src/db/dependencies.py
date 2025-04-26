from fastapi import Request
from sqlalchemy.orm.session import Session as SessionLocal


async def get_db(request: Request):
    session: SessionLocal = getattr(request.state, "db")
    yield session
