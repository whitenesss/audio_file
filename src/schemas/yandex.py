from dataclasses import dataclass
from enum import StrEnum
from typing import Union
from uuid import UUID

from pydantic import BaseModel, EmailStr


class OAuthServices(StrEnum):
    yandex = "yandex"

@dataclass(frozen=True, slots=True)
class UserOAuthData:
    service_name: OAuthServices
    user_service_id: Union[str, int]
    email: str
    username: str


class UserCreateSocialSite(BaseModel):
    email: EmailStr
    uid: UUID
    username: str

class UserCreateYandex(UserCreateSocialSite):
    yandex_id: int