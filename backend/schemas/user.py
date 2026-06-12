from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime, date
from uuid import UUID
import re

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=100)
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v): raise ValueError('Ən azı 1 böyük hərf olmalıdır')
        if not re.search(r"[a-z]", v): raise ValueError('Ən azı 1 kiçik hərf olmalıdır')
        if not re.search(r"\d", v): raise ValueError('Ən azı 1 rəqəm olmalıdır')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: UUID; username: str; email: str; full_name: str
    rating: int; max_rating: int; total_solved: int; total_points: int
    role: str; is_verified: bool; avatar_url: Optional[str] = None
    country: Optional[str] = None; created_at: datetime
    class Config: from_attributes = True

class TokenResponse(BaseModel):
    access_token: str; refresh_token: str; token_type: str = "bearer"
    expires_in: int; user: UserResponse
