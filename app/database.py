# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# 使用 SQLite 資料庫 (phantom_mask.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./phantom_mask.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
