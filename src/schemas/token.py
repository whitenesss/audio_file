from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from typing import TypeVar

from starlette.responses import Response

ResponseT = TypeVar("ResponseT", bound=Response)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenAccessRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    uid: UUID

class AuthURLResponse(BaseModel):
    url: str




