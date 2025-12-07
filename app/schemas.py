from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token: str


class DataRecordBase(BaseModel):
    title: str
    category: Optional[str]
    payload: Optional[str]


class DataRecordCreate(DataRecordBase):
    created_by: int


class DataRecordOut(DataRecordBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True