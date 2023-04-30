from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.db import config

SQLALCHEMY_DATABASE_URL = config.get_settings().database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


# Database utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache()
def get_settings():
    return config.Settings()



