import re
from datetime import datetime
from typing import Union, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator
from pydantic import EmailStr
from pydantic.networks import validate_email

MIN_PASSWORD_LENGTH = 8


class UserBase(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True




class PasswordBase(BaseModel):
    password: str = Field(..., min_length=8)

    @validator("password")
    def password_validation(cls, v: str) -> str:
        if len(v) < MIN_PASSWORD_LENGTH or not re.match(r"^[ -~]+$", v):
            msg = "Password does not meet the requirements."
            raise ValueError(msg)
        return v


class UserCreate(PasswordBase, UserBase):
    pass


class UserResponse(UserBase):
    uid: UUID
    username: Optional[str] = None


class UserCreateDB(UserBase):
    uid: UUID
    hashed_password: str
