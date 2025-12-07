from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from passlib.context import CryptContext
from datetime import datetime
import re

from . import models, schemas

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def validate_password_strength(password: str):
    """
    Raises ValueError when password does not meet strength rules.
    Rules:
    - Minimum 8 characters
    - At least one letter
    - At least one number
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    if not re.search(r"[A-Za-z]", password):
        raise ValueError("Password must contain at least one letter")

    if not re.search(r"[0-9]", password):
        raise ValueError("Password must contain at least one number")



def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None

    # Correct verification using argon2
    if not pwd_context.verify(password, user.hashed_password):
        return None

    return user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()



def create_user(db: Session, user: schemas.UserCreate) -> models.User:

    # 1. Duplicate email check (explicit)
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise ValueError("Email already registered")

    # 2. Password validation
    validate_password_strength(user.password)

    # 3. Hash password
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(db_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered")  # fallback

    db.refresh(db_user)
    return db_user


def create_record(db: Session, record: schemas.DataRecordCreate) -> models.DataRecord:
    db_record = models.DataRecord(
        title=record.title,
        category=record.category,
        payload=record.payload,
        created_by=record.created_by,
    )

    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return db_record


def list_records(db: Session, limit: int = 50, skip: int = 0):
    return (
        db.query(models.DataRecord)
        .order_by(models.DataRecord.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def search_records(db: Session, category: str = None, start_date: datetime = None, end_date: datetime = None):
    query = db.query(models.DataRecord)

    if category:
        query = query.filter(models.DataRecord.category == category)

    if start_date:
        query = query.filter(models.DataRecord.created_at >= start_date)

    if end_date:
        query = query.filter(models.DataRecord.created_at <= end_date)

    return (
        query.order_by(models.DataRecord.created_at.desc())
        .all()
    )


def record_stats(db: Session):
    rows = (
        db.query(
            models.DataRecord.category,
            func.count(models.DataRecord.id).label("count"),
            func.max(models.DataRecord.created_at).label("latest"),
        )
        .group_by(models.DataRecord.category)
        .all()
    )

    
    stats = {}
    for category, count, latest in rows:
        stats[category] = {
            "count": count,
            "latest": latest,
        }

    return stats
