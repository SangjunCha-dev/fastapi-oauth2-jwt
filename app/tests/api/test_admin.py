import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.users import UserCreateSchema
from app.crud.users import crud_user
from app.tests.utils.utils import *


def test_get_user_superuser_me(
    client: TestClient,
    superuser_token_headers: dict[str, str],
) -> None:
    response = client.get(f"/admin/users/me", headers=superuser_token_headers)
    current_user = response.json()

    assert response.status_code == 200
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL


def test_get_users(
    db: Session,
    client: TestClient,
    superuser_token_headers: dict,
) -> None:

    count = 2
    for _ in range(count):
        user_in = UserCreateSchema(
            email=random_email(), 
            password=random_password(),
            name=random_name(),
            age=random_age(),
        )
        crud_user.create(db, obj_in=user_in)

    response = client.get(f"/admin/users", headers=superuser_token_headers)
    all_users = response.json()

    assert response.status_code == 200
    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user


def test_get_user(
    db: Session,
    client: TestClient,
    superuser_token_headers: dict,
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
    user = crud_user.create(db, obj_in=user_in)

    response = client.get(f"/admin/users/{user.id}", headers=superuser_token_headers)

    assert 200 <= response.status_code < 300

    response_json = response.json()
    get_user = crud_user.get_by_email(db, email=email)

    assert get_user
    assert get_user.email == response_json["email"]
    assert get_user.name == response_json["name"]
    assert get_user.age == response_json["age"]


def test_create_user_by_normal_user(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
) -> None:
    data = {
        "email": random_email(),
        "password": random_password(),
        "name": random_name(),
        "age": random_age(),
    }

    response = client.post("/admin/users", headers=normal_user_token_headers, json=data)
    response_json = response.json()

    assert response.status_code == 400
    assert "detail" in response_json


def test_update_user(
    db: Session,
    client: TestClient,
    superuser_token_headers: dict[str, str],
) -> None:

    get_user = crud_user.get_by_email(db, email=settings.TEST_USER_EMAIL)

    name = random_name()
    age = random_age()
    data = {
        "name": name,
        "age": age,
    }

    response = client.put(f"/admin/users/{get_user.id}", headers=superuser_token_headers, json=data)
    updated_user = response.json()

    assert response.status_code == 200
    assert updated_user
    assert updated_user["email"] == settings.TEST_USER_EMAIL
    assert updated_user["name"] == name
    assert updated_user["age"] == age
