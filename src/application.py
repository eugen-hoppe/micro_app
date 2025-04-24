from fastapi import FastAPI, Request, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from src.db.models import Base
from src.apps.subscription.endpoints import subscription_api


app = FastAPI(
    title="Micro App API",
    description="App Development Template",
    version="1.0",
)


sql_url = "sqlite:///./sql_app.db"
engine = create_engine(url=sql_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


app.include_router(subscription_api, prefix="/api")

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        setattr(request.state, "db", SessionLocal())
        response = await call_next(request)
    finally:
        session: Session = getattr(request.state, "db")
        session.close()
    return response
