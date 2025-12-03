from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://umj9n8yetht8bxe6sgzw:1LOfHqPYTKhB0C0QcMTY2HRtHUD6Lv@bauv12qjdizjgv7pb4yz-postgresql.services.clever-cloud.com:50013/bauv12qjdizjgv7pb4yz"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()