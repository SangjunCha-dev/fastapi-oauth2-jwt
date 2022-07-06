import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.users import UserCreateSchema
from app.crud.users import crud_user
from app.tests.utils.utils import *


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


def test_create_user(
    client: TestClient,
) -> None:
    email = random_email()
    password = random_password()
    name = random_name()
    age = random_age()

    data = {
        "email": email, 
        "password": password,
        "name": name,
        "age": age,
    }
    response = client.post("/users", json=data)

    assert 200 <= response.status_code < 300

    response_json = response.json()

    assert response_json["email"] == email
    assert response_json["name"] == name
    assert response_json["age"] == age


def test_create_user_duplicate_email(
    db: Session,
    client: TestClient,
) -> None:
    email = random_email()
    password = random_password()
    name = random_name()
    age = random_age()
    user_in = UserCreateSchema(
        email=email, 
        password=password,
        name=name,
        age=age,
    )
    crud_user.create(db, obj_in=user_in)

    data = {
        "email": email, 
        "password": password,
        "name": name,
        "age": age,
    }
    response = client.post("/users", json=data)
    response_json = response.json()

    assert response.status_code == 400
    assert "detail" in response_json


def test_update_user(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
) -> None:
    name = random_name()
    age = random_age()
    data = {
        "name": name,
        "age": age,
    }

    response = client.put(f"/users", headers=normal_user_token_headers, json=data)
    updated_user = response.json()

    assert response.status_code == 200
    assert updated_user
    assert updated_user["email"] == settings.TEST_USER_EMAIL
    assert updated_user["name"] == name
    assert updated_user["age"] == age
