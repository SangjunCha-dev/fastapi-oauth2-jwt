from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.items import create_random_item
from app.core.config import settings
from app.crud.users import crud_user
from app.tests.utils.utils import random_name, random_number, random_lower_string


def test_create_item(
    client: TestClient,
    normal_user_token_headers: dict,
) -> None:
    data = {
        "name": "product1",
        "description": "product_description1",
        "price": 1000,
        "quantity": 10,
    }
    response = client.post("/items", headers=normal_user_token_headers, json=data)

    assert response.status_code == 201

    content = response.json()

    assert "id" in content
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["price"] == data["price"]
    assert content["quantity"] == data["quantity"]
    assert "owner_id" in content


def test_get_item(
    db: Session,
    client: TestClient,
    normal_user_token_headers: dict,
) -> None:
    user = crud_user.get_by_email(db, email=settings.TEST_USER_EMAIL)

    item = create_random_item(db, owner_id=user.id)
    response = client.get(f"/items/{item.id}", headers=normal_user_token_headers)

    assert response.status_code == 200

    content = response.json()

    assert content["id"] == item.id
    assert content["name"] == item.name
    assert content["description"] == item.description
    assert content["price"] == item.price
    assert content["quantity"] == item.quantity
    assert content["owner_id"] == item.owner_id


def test_get_items(
    db: Session,
    client: TestClient,
    normal_user_token_headers: dict,
) -> None:
    user = crud_user.get_by_email(db, email=settings.TEST_USER_EMAIL)

    count = 10
    for _ in range(count):
        create_random_item(db, owner_id=user.id)

    skip = 0
    limit = 5
    response = client.get(f"/items?skip={skip}&limit={limit}", headers=normal_user_token_headers)

    assert response.status_code == 200

    all_items = response.json()

    assert len(all_items) == limit
    for item in all_items:
        assert "name" in item
        assert "description" in item
        assert "price" in item
        assert "quantity" in item
        assert "owner_id" in item


def test_update_item(
    db: Session,
    client: TestClient,
    normal_user_token_headers: dict,
) -> None:
    user = crud_user.get_by_email(db, email=settings.TEST_USER_EMAIL)
    item = create_random_item(db, owner_id=user.id)
    
    data = {
        "name": random_name(),
        "description": random_lower_string(100),
        "price": random_number(),
        "quantity": random_number(),
    }
    response = client.put(f"/items/{item.id}", headers=normal_user_token_headers, json=data)

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["price"] == data["price"]
    assert content["quantity"] == data["quantity"]


def test_delete_item(
    db: Session,
    client: TestClient,
    normal_user_token_headers: dict,
) -> None:
    user = crud_user.get_by_email(db, email=settings.TEST_USER_EMAIL)
    item = create_random_item(db, owner_id=user.id)

    response = client.delete(f"/items/{item.id}", headers=normal_user_token_headers)

    assert response.status_code == 200

    content = response.json()

    assert content["id"] == item.id