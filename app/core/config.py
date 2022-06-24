import os
from pathlib import Path
import json
import sys
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # minutes * hours * days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    TOKEN_URL = "/login/access-token"

    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl

    # 사용자 회원가입 On/Off
    USERS_OPEN_REGISTRATION: bool = True

    # read settings
    CONFIG_ROOT = Path(__file__).resolve().parent
    config_filename = 'secrets.json'
    config_file = os.path.join(CONFIG_ROOT, config_filename)
    config = json.loads(open(config_file).read())
    for key, value in config.items():
        setattr(sys.modules[__name__], key, value)

    PROJECT_NAME = PROJECT_NAME
    CORS_ORIGINS = CORS_ORIGINS

    # database connection
    DATABASE_USER = DATABASE['USER']
    DATABASE_PASSWORD = DATABASE['PASSWORD']
    DATABASE_HOST = DATABASE['HOST']
    DATABASE_PORT = DATABASE['PORT']
    DATABASE_NAME = DATABASE['DB_NAME']
    SQLALCHEMY_DATABASE_URL=f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    # super user info
    FIRST_SUPERUSER_EMAIL = FIRST_SUPERUSER_EMAIL
    FIRST_SUPERUSER_PASSWORD = FIRST_SUPERUSER_PASSWORD
    TEST_USER_EMAIL = "tester@example.com"


settings = Settings()