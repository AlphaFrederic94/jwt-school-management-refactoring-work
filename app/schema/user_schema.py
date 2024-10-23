# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: str
    date_of_birth: Optional[date] = None

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    date_of_birth: Optional[date]

    class Config:
        orm_mode = True