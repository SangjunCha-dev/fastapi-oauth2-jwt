from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }

    response = client.post(settings.TOKEN_URL, data=login_data)
    response_json = response.json()

    assert response.status_code == 200
    assert "access_token" in response_json
    assert response_json["access_token"]


def test_use_access_token(
    client: TestClient, 
    superuser_token_headers: dict[str, str],
) -> None:
    response = client.post(f"/login/test-token", headers=superuser_token_headers)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["email"] == settings.FIRST_SUPERUSER_EMAIL
    assert "name" in response_json
    assert "age" in response_json
    assert "items" in response_json
    assert "hashed_password" not in response_json
    assert "password" not in response_json
