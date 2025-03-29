from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base
load_dotenv()
BASE_DIR = Path(__file__).parent.parent


class BaseSetting(BaseSettings):
    class Config:
        env_file_encoding = "UTF-8"
        extra = "allow"

class DBSettings(BaseSetting):
    POSTGRES_HOST_ALEMBIC: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

class JWTSettings(BaseSetting):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES: int  # minutes
    JWT_REFRESH_TOKEN_EXPIRES: int  # minutes

class YandexSetting(BaseSetting):
    YANDEX_APP_ID: str
    YANDEX_CLIENT_SECRET: str


YANDEX_AUTH_BASE_URL = "https://oauth.yandex.ru/authorize?"
YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"
YANDEX_USER_INFO_URL = "https://login.yandex.ru/info"
YANDEX_REDIRECT_URI = "https://verification_code/"

Base = declarative_base()


yandex_settings = YandexSetting()
db_settings = DBSettings()
jwt_settings = JWTSettings()
