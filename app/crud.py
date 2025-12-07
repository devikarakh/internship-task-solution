from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if user.hashed_password != password:
        return None
    return user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
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