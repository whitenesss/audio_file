from datetime import timedelta

from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearer

from src.conf import jwt_settings

access_security = JwtAccessBearerCookie(
    secret_key=jwt_settings.JWT_SECRET_KEY,
    access_expires_delta=timedelta(
        minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRES
    ),
)
access_security_optional = JwtAccessBearerCookie(
    secret_key=jwt_settings.JWT_SECRET_KEY,
    auto_error=False,
    access_expires_delta=timedelta(
        minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRES
    ),
)

refresh_security = JwtRefreshBearer(
    secret_key=jwt_settings.JWT_SECRET_KEY,
    refresh_expires_delta=timedelta(
        minutes=jwt_settings.JWT_REFRESH_TOKEN_EXPIRES
    ),
)


ACCESS_TOKEN_COOKIE_KEY = "access_token_cookie"
REFRESH_TOKEN_COOKIE_KEY = "refresh_token_cookie"
