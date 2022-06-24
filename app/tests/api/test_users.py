import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.users import UserCreateSchema
from app.crud.users import crud_user
from app.tests.utils.utils import *


def test_get_user_superuser_me(
    client: TestClient,
    superuser_token_headers: dict[str, str],
) -> None:
    response = client.get(f"/users/me", headers=superuser_token_headers)
    current_user = response.json()

    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL


def test_get_user_normal_me(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
) -> None:
    response = client.get(f"/users/me", headers=normal_user_token_headers)
    current_user = response.json()

    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.TEST_USER_EMAIL
