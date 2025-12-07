import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://intern:intern@localhost:3306/internship_task",
)

# --- Improvement #1: handle DB connection errors ---
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
except OperationalError as e:
    print("❌ Database connection failed:", e)
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
