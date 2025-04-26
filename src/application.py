from __future__ import annotations
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastcrud import crud_router
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.conf import settings
from src.core.database import engine, Base, get_session
from src.models.subscription import Subscription
from src.models.user import User
from src.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from src.schemas.user import UserCreate, UserUpdate
from src.core.web import web_app



async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Micro App API – FastCRUD edition",
    description="Refactor using FastCRUD for generic CRUD ops",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

subscription_router = crud_router(
    session=get_session,
    model=Subscription,
    create_schema=SubscriptionCreate,
    update_schema=SubscriptionUpdate,
    path=f"{settings.API_PREFIX}/subscription",
    tags=["plan"],
)

user_router = crud_router(
    session=get_session,
    model=User,
    create_schema=UserCreate,
    update_schema=UserUpdate,
    path=f"{settings.API_PREFIX}/user",
    tags=["user"],
)

app.include_router(subscription_router)
app.include_router(user_router)
app.include_router(web_app)
