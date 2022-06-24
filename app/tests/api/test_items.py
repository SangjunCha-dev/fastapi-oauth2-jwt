from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.items import create_random_item



def test_read_item(
    db: Session,
    client: TestClient,
    superuser_token_headers: dict,
) -> None:
    item = create_random_item(db)
    response = client.get(f"/items/{item.id}", headers=superuser_token_headers)

    assert response.status_code == 200

    content = response.json()

    assert content["id"] == item.id
    assert content["name"] == item.name
    assert content["description"] == item.description
    assert content["price"] == item.price
    assert content["quantity"] == item.quantity
    assert content["owner_id"] == item.owner_id
