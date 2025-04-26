from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from src.apps.subscription.endpoints import subscription_api
from src.apps.user.endpoints import user_api
from src.apps.web import web_app
from src.db.generic import Base
from src.settings.conf import DATABASE_URL, PREFIX


engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


async def _ensure_schema_exists() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _ensure_schema_exists()
    yield


app = FastAPI(
    title="Micro App API",
    description="App Development Template (refactored)",
    version="1.1.0",
    response_model_exclude_none=True,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    async with AsyncSessionLocal() as session:
        request.state.db = session
        try:
            response = await call_next(request)
            await session.commit()
            return response
        except Exception:
            await session.rollback()
            raise


app.include_router(subscription_api, prefix=PREFIX)
app.include_router(user_api, prefix=PREFIX)
app.include_router(web_app)
