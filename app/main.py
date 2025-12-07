from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, schemas, crud
from .database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Internship Task API", version="0.1.0")


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/auth/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user


@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"token": f"debug-token-for-{user.email}"}


@app.post("/records", response_model=schemas.DataRecordOut, status_code=status.HTTP_201_CREATED)
def create_record(record: schemas.DataRecordCreate, db: Session = Depends(get_db)):
    return crud.create_record(db, record)


@app.get("/records", response_model=List[schemas.DataRecordOut])
def list_records(limit: int = 50, skip: int = 0, db: Session = Depends(get_db)):
    return crud.list_records(db, limit=limit, skip=skip)


@app.get("/records/stats")
def record_statistics(db: Session = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Implement aggregation task")