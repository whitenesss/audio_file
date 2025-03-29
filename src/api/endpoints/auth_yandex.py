from typing import Optional
from uuid import UUID
from starlette.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, Depends

from src.conf import YANDEX_AUTH_BASE_URL, yandex_settings
from src.database import get_async_db
from src.schemas.token import AuthURLResponse, TokenAccessRefresh
from src.schemas.yandex import UserCreateYandex
from src.services.token import create_tokens, set_tokens_to_cookie
from src.services.yndex import get_yandex_oauth_data, get_or_create_oauth_user

router = APIRouter(prefix="/yandex", tags=["yandex"])

@router.get("/start/", response_model=AuthURLResponse)
async def start_auth(user_uid: Optional[UUID] = None) -> AuthURLResponse:
    if not yandex_settings.YANDEX_APP_ID:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Yandex Auth is not configured yet",
        )
    auth_url = (
        f"{YANDEX_AUTH_BASE_URL}"
        f"client_id={yandex_settings.YANDEX_APP_ID}&"
        f"display=page&"
        f"scope=login:email login:info&"
        f"response_type=code&"
        f"v=1.0&"
        f"state={user_uid}"
    )
    return AuthURLResponse(url=auth_url)


@router.get("/callback/", response_model=TokenAccessRefresh)
async def yandex_callback(
        code: str,
        state: Optional[UUID] = None,
        db: AsyncSession = Depends(get_async_db),
):
    user_data = await get_yandex_oauth_data(code=code)

    user = await get_or_create_oauth_user(
        db=db,
        user_uid=state,
        user_data=user_data,
        schema_type=UserCreateYandex,
    )

    tokens = await create_tokens(subject={"uid": str(user.uid)})
    response = JSONResponse(content=tokens.model_dump())
    return await set_tokens_to_cookie(response=response, tokens=tokens)

