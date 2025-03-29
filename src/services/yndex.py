from enum import StrEnum
from typing import Optional, Dict, Any, Union, Type
from dataclasses import dataclass
from uuid import uuid4

import httpx
from httpx import HTTPStatusError
from sqlalchemy.ext.asyncio import AsyncSession




from src.conf import yandex_settings, YANDEX_REDIRECT_URI, YANDEX_TOKEN_URL, YANDEX_USER_INFO_URL
from src.crud.user import crud_user
from src.models import User
from src.schemas.yandex import UserOAuthData, OAuthServices, UserCreateSocialSite

HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}





async def get_oauth_user_token(
    client: httpx.AsyncClient,
    token_url: str,
    data: Optional[dict] = None,
    params: Optional[dict] = None,
    headers: Optional[dict] = None,
) -> Dict[str, Any]:
    response = await client.post(
        url=token_url, data=data, params=params, headers=headers
    )
    try:
        response.raise_for_status()
    except HTTPStatusError as ex:
        raise HTTPStatusError(
            message=str(response.content),
            response=response,
            request=response.request,
        ) from ex
    return response.json()

async def get_oauth_user_data(
    client: httpx.AsyncClient,
    params: dict,
    user_info_url: str,
    headers: Optional[dict] = None,
) -> Dict[str, Any]:
    response = await client.get(
        url=user_info_url, params=params, headers=headers
    )
    try:
        response.raise_for_status()
    except HTTPStatusError as ex:
        raise HTTPStatusError(
            message=str(response.content),
            response=response,
            request=response.request,
        ) from ex
    return response.json()


async def get_yandex_oauth_data(code: str) -> UserOAuthData:
    data = {
        "client_id": yandex_settings.YANDEX_APP_ID,
        "client_secret": yandex_settings.YANDEX_CLIENT_SECRET,
        "redirect_uri": YANDEX_REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_data = await get_oauth_user_token(
            client=client,
            data=data,
            token_url=YANDEX_TOKEN_URL,
            headers=HEADERS,
        )
        params = {
            "format": "json",
        }
        headers = {"Authorization": f"OAuth {token_data['access_token']}"}
        user_raw_data = await get_oauth_user_data(
            client=client,
            params=params,
            user_info_url=YANDEX_USER_INFO_URL,
            headers=headers,
        )

    return UserOAuthData(
        service_name=OAuthServices.yandex,
        user_service_id=int(user_raw_data.get("id")),
        email=user_raw_data.get("default_email"),
        username=user_raw_data.get("first_name", ""),

    )

async def get_or_create_oauth_user(
    db: AsyncSession,
    user_data: UserOAuthData,
    schema_type: Type[UserCreateSocialSite],
    user_uid: Optional[str],
) -> User:
    if user_uid:
        return await process_adding_oauth(
            db=db, user_data=user_data, user_uid=user_uid
        )
    return await process_registration_and_login(
        db=db, user_data=user_data, schema_type=schema_type
    )


async def process_adding_oauth(
    db: AsyncSession,
    user_data: UserOAuthData,
    user_uid: str,
) -> User:
    found_user = await crud_user.get_by_uid(db, uid=user_uid)


    service_name = user_data.service_name
    service_id_field = f"{service_name}_id"
    user_service_id = user_data.user_service_id
    found_user_with_service_id = await crud_user.get_by_service_id(
        db=db,
        service_id_field=service_id_field,
        user_service_id=user_service_id,
    )
    # if found_user_with_service_id:
    #     msg = f"{service_name.capitalize()} account already in use."
    #     raise PermissionDeniedError(msg)
    # if getattr(found_user, service_id_field):
    #     msg = "Oauth already connected. Remove current to connect new."
    #     raise PermissionDeniedError(msg)
    # setattr(found_user, service_id_field, user_service_id)
    await db.commit()
    return found_user


async def process_registration_and_login(
    db: AsyncSession,
    user_data: UserOAuthData,
    schema_type: Type[UserCreateSocialSite],
) -> User:
    service_name = user_data.service_name
    service_id_field = f"{service_name}_id"
    user_service_id = user_data.user_service_id

    found_user_with_service_id = await crud_user.get_by_service_id(
        db=db,
        service_id_field=service_id_field,
        user_service_id=user_service_id,
    )
    if found_user_with_service_id:
        return found_user_with_service_id
    new_user = await create_oauth_user(
        db=db, user_data=user_data, schema_type=schema_type
    )


    return new_user


async def create_oauth_user(
    db: AsyncSession,
    user_data: UserOAuthData,
    schema_type: Type[UserCreateSocialSite],
) -> User:
    user_service_id = user_data.user_service_id
    service_name = user_data.service_name
    service_id_field = f"{service_name}_id"

    uid = uuid4()
    new_user_data = {
        service_id_field: user_service_id,
        "uid": uid,
        "email": user_data.email,
        "username": user_data.username,
    }
    new_user: User = await crud_user.create(
        db=db, create_schema=schema_type(**new_user_data)
    )
    new_user.contact_emails = [user_data.email]
    await db.commit()
    await db.refresh(new_user)
    return new_user