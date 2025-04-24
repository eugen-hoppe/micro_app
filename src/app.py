from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session



app = FastAPI(
    title="Micro App API",
    description="App Development Template",
    version="1.0",
)


sql_url = "sqlite:///./sql_app.db"
engine = create_engine(url=sql_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)
