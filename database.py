import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Si Render tiene DATABASE_URL, úsala. Si no, usa la fija de Clever Cloud.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://uyfwrbo579r56bazkvpe:fY4dymWS8N1bOKhpMQCdshFUVIfb81@b9snz55bmuviqhb7nkhv-postgresql.services.clever-cloud.com:50013/b9snz55bmuviqhb7nkhv"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
