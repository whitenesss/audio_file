

from datetime import timedelta
from typing import TypedDict, Union
from uuid import UUID
from src.conf import jwt_settings
from src.schemas.token import TokenAccessRefresh, ResponseT
from src.services.security import access_security, refresh_security, ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY



class TokenSubject(TypedDict):
    uid: Union[UUID, str]


async def create_tokens(subject: TokenSubject) -> TokenAccessRefresh:
    access_token = await create_access_token(subject)
    refresh_token = await create_refresh_token(subject)
    return TokenAccessRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


async def create_access_token(subject: TokenSubject) -> str:
    return access_security.create_access_token(subject=subject)


async def create_refresh_token(subject: TokenSubject) -> str:
    return refresh_security.create_refresh_token(
        subject=subject,
        expires_delta=timedelta(
            minutes=jwt_settings.JWT_REFRESH_TOKEN_EXPIRES
        ),
    )

async def set_tokens_to_cookie(
    response: ResponseT, tokens: TokenAccessRefresh
) -> ResponseT:
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_KEY,
        value=tokens.access_token,
        secure=True,
        httponly=True,
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_KEY,
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
    )
    return response